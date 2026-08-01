# EDR-003: Why a Decorator for Retry Logic

## Status
Accepted

## Problem
ScraperFlow V3 needs retry logic for transient network failures (timeouts, 5xx, connection resets). Where should this logic live, and what mechanism should implement it?

## Context
Running V2 against real sites surfaces repeated transient failures. Without a retry policy, a single timeout kills the entire run. The retry behavior is identical regardless of what URL is being fetched — it only cares about the failure type, not the content. This makes it a cross-cutting concern: functionality that applies uniformly across many components but isn't part of any one component's core responsibility.

## Possible Solutions
1. **Inline `try/except` with a loop at each call site** — every function that does network I/O contains its own retry loop.
2. **`RetryMixin` base class** — a mixin that subclasses override to get retry behavior.
3. **`@retry` decorator factory** — a decorator applied to functions that need retry, with configurable `max_attempts`, `base_delay`, and `max_delay`.
4. **External library (`tenacity`)** — use a production-grade retry library instead of building one.

## Chosen Solution
Option 3 — `@retry` decorator factory in `scraperflow/retry.py`.

## Why This Solution Was Selected
- **Retry operates at the function boundary.** It wraps the entire call, catches a specific exception type, and decides whether to call again. This is exactly the pattern a decorator provides.
- **One definition, applied declaratively.** `@retry(max_attempts=3)` on `fetch_page` reads as "this function should be retried" without cluttering its body. The retry policy lives in exactly one place — changing backoff strategy or max attempts is a single-line edit.
- **Testable in isolation.** The decorator can be tested with trivial stub functions that fail N times then succeed, with `time.sleep` monkeypatched. No network, no HTML, no parsing — just retry behavior.
- **Clean separation from the exception hierarchy.** The decorator catches `TransientFetchError` (defined in `exceptions.py`). The fetcher raises `TransientFetchError` (translating from `requests` exceptions). Neither knows about the other's internals — the exception type is the contract between them.

## Trade-offs Accepted
- Building a custom decorator instead of using `tenacity` means maintaining ~15 lines of retry logic ourselves. Acceptable at this scale — the decorator is simple, well-tested, and a learning objective for this week.
- The decorator is hardcoded to catch `TransientFetchError`. If a future version needs retry on a different exception type, the `retry_on` parameter (stretch goal) would generalize it.

## Why Alternatives Were Rejected
- **Option 1 (inline)** duplicates the retry loop in every function that does I/O. Each copy drifts: different attempt counts, different backoff formulas, different exception handling. Untestable in isolation. Violates DRY.
- **Option 2 (mixin)** requires an inheritance hierarchy just to add retry behavior. Too heavyweight — retry doesn't need access to instance state. Functions that aren't methods can't use it. Forces a class structure where none is needed.
- **Option 4 (`tenacity`)** is the right choice for production systems with complex retry needs (per-exception backoff, circuit breakers, retry budgets). For V3's scope — one exception type, one backoff strategy, five call sites — it adds a dependency without meaningful benefit over 15 lines of code. Revisit if retry requirements grow.

## When to Revisit
- If multiple exception types need different retry strategies (e.g., `RateLimitError` with longer backoff than `TimeoutError`), consider adding a `retry_on` parameter or switching to `tenacity`.
- If V10's distributed system needs circuit breaker patterns alongside retry, `tenacity` or a dedicated resilience library becomes worth the dependency.
