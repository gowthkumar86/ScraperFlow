# Week 03 Implementation Guide — ScraperFlow V3: Retry & Resilience

## Objective

Handle transient failures (timeouts, 5xx, connection resets) with one consistent, tested policy instead of ad hoc `try/except` per scraper. A small exception hierarchy classifies failure by type, and a `@retry` decorator catches narrowly — only failures actually worth retrying — with exponential backoff plus jitter.

## What Broke (Why This Version Exists)

Running V2 for real surfaces genuine, repeated network failures. Without a retry policy, a single transient timeout kills the entire run. Ad hoc `try/except` blocks scattered through the code would be inconsistent, hard to test, and impossible to tune globally. The question isn't "how do I implement retry" — it's "what kind of thing *is* retry logic, conceptually?" It's a cross-cutting concern that applies uniformly regardless of what's being fetched.

## Requirements

1. A custom exception hierarchy: `ScraperFlowError` (base) → `FetchError` → `TransientFetchError` / `PermanentFetchError`
2. A `@retry` decorator that:
   - Retries only on `TransientFetchError` (not `PermanentFetchError`, not other exceptions)
   - Uses exponential backoff with full jitter between attempts
   - Has a configurable maximum number of attempts (default 3)
   - Raises the last `TransientFetchError` if all attempts are exhausted
   - Logs each retry attempt (attempt number, delay, error message)
3. The decorator must be a **decorator factory** (accepts `max_attempts` and optionally `base_delay` as parameters)
4. `fetcher.py` raises `TransientFetchError` for 5xx status codes, timeouts, and connection errors
5. `fetcher.py` raises `PermanentFetchError` for 4xx status codes (the resource genuinely doesn't exist)
6. The `@retry` decorator is applied to the fetch function — retry logic lives in exactly one place
7. All V1/V2 tests still pass

## Architecture Decisions to Make

- **Should the exception hierarchy live in its own module (`exceptions.py`) or inside `fetcher.py`?** Consider: the hierarchy will be imported by multiple modules in later versions (V6 adds `StorageError`, V7's Worker uses these types for requeue decisions). Where should shared vocabulary live?
- **Decorator factory vs. simple decorator?** A simple `@retry` with hardcoded config, or `@retry(max_attempts=3, base_delay=1.0)` with configurable parameters? Consider: will different call sites ever need different retry policies?
- **Full jitter vs. equal jitter vs. decorrelated jitter?** Pick one and document why. (Hint: AWS's analysis shows full jitter provides the best spread for most use cases.)
- **Should the decorator preserve the wrapped function's signature and docstring?** (Yes — use `functools.wraps`. Decide and understand why.)
- **What HTTP status codes count as transient vs. permanent?** 429 (Too Many Requests) is transient. 404 is permanent. What about 403? Make a decision and document it.

## Acceptance Criteria

- [ ] `TransientFetchError` and `PermanentFetchError` exist as distinct exception classes with a shared base
- [ ] `@retry` decorator retries on `TransientFetchError` only
- [ ] `@retry` decorator does NOT retry on `PermanentFetchError`
- [ ] `@retry` decorator does NOT retry on unexpected exceptions (e.g., `TypeError`, `ValueError`)
- [ ] Backoff includes jitter (delays are not identical across attempts)
- [ ] Maximum attempt count is configurable and honored
- [ ] After exhausting all attempts, the original exception is re-raised (not swallowed)
- [ ] Retry logic exists in exactly one place (the decorator), not duplicated per call site
- [ ] Decorated functions preserve their `__name__`, `__doc__`, and `__module__` (`functools.wraps`)
- [ ] Test suite runs in well under a second (no real `time.sleep` during tests)

## Tests to Write

- [ ] `test_retry_succeeds_on_first_attempt` — function succeeds without retry, decorator is transparent
- [ ] `test_retry_succeeds_after_transient_failure` — function fails once with `TransientFetchError`, then succeeds on second attempt
- [ ] `test_retry_exhausts_max_attempts` — function always raises `TransientFetchError`, decorator gives up after `max_attempts` and re-raises
- [ ] `test_retry_does_not_catch_permanent_error` — function raises `PermanentFetchError`, decorator does NOT retry, exception propagates immediately
- [ ] `test_retry_does_not_catch_unexpected_error` — function raises `ValueError`, decorator does NOT retry
- [ ] `test_retry_applies_backoff_with_jitter` — monkeypatch `time.sleep` and verify that sleep durations increase (approximately exponentially) and are not identical
- [ ] `test_retry_preserves_function_metadata` — decorated function's `__name__` and `__doc__` match the original
- [ ] `test_fetcher_raises_transient_on_5xx` — fetcher raises `TransientFetchError` for 500, 502, 503, 504
- [ ] `test_fetcher_raises_permanent_on_4xx` — fetcher raises `PermanentFetchError` for 404, 410
- [ ] `test_fetcher_raises_transient_on_timeout` — fetcher raises `TransientFetchError` on connection timeout

## Refactoring Checkpoint

- [ ] Centralize any ad hoc `try/except` error handling left over from V1/V2 — remove scattered exception handling and replace with the new hierarchy
- [ ] Ensure `fetcher.py` raises typed exceptions instead of letting raw `requests` exceptions propagate
- [ ] Verify that `Scraper` (from V2) doesn't need to know about retry logic — the decorator handles it at the fetch layer

## EDR to Write

**EDR-003: Why a Decorator for Retry Logic** — Document why retry is implemented as a `@retry` decorator applied to the fetch function, rather than: (a) inline `try/except` with a loop at each call site, (b) a `RetryMixin` base class, or (c) an external library like `tenacity`. Address: what makes retry a cross-cutting concern, why decorators are the right tool for cross-cutting concerns, and when you'd reach for `tenacity` instead.

## Files to Create / Modify

- `scraperflow/exceptions.py` — Exception hierarchy: `ScraperFlowError` → `FetchError` → `TransientFetchError` / `PermanentFetchError`
- `scraperflow/retry.py` — `@retry` decorator factory with exponential backoff and jitter
- `scraperflow/fetcher.py` — Modified to raise typed exceptions instead of letting raw `requests` exceptions propagate
- `tests/test_retry.py` — Tests for the retry decorator in isolation
- `tests/test_fetcher.py` — Tests for exception classification in fetcher

## Done When

One tested retry decorator applied consistently, and the suite still runs in well under a second despite testing multi-attempt logic. The exception hierarchy is the shared vocabulary — `TransientFetchError` means "worth retrying," `PermanentFetchError` means "don't bother."

## Watch For

- **Catching too broadly inside the decorator** — only `TransientFetchError` should trigger a retry. Catching `Exception` means you'll retry on `TypeError` from a bug in your own code.
- **No maximum attempt count** — infinite retry loops are a production incident waiting to happen.
- **No backoff at all** — retrying immediately N times in a row hammers an already-struggling server.
- **Backoff without jitter** — synchronized retries from multiple workers create a "thundering herd." Jitter spreads them out.
- **Swallowing the exception after exhaustion** — if all retries fail, the caller must know. Re-raise, don't return `None`.
- **Retrying permanent failures** — a 404 will still be a 404 on the second attempt. Classify failures correctly.

## Stretch Goals

- Add a `retry_on` parameter to the decorator factory that accepts a tuple of exception types (not just hardcoded `TransientFetchError`)
- Add an `on_retry` callback parameter for custom logging or metrics
- Implement decorrelated jitter as an alternative strategy and compare the spread
