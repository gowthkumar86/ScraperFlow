# Week 04 — Self-Review Checklist

Work through each section below against your actual V1–V3 codebase. The goal is not to achieve perfection — it's to surface implicit decisions, identify drift between intent and reality, and find anything that should be documented or cleaned up before V4 introduces new abstraction layers.

---

## 1. Module Layout & Responsibility Boundaries (EDR-001)

- [ ] Does each module (`fetcher.py`, `parser.py`, `storage.py`, `config.py`, `retry.py`, `scraper.py`, `cli.py`, `exceptions.py`) have exactly one reason to change?
- [ ] Are there any functions that ended up in the "wrong" module? (e.g., parsing logic in fetcher, formatting in storage)
- [ ] Does `__init__.py` expose a clean public API, or does it import everything indiscriminately?
- [ ] Could a new developer find the retry logic by filename alone? The config? The exceptions?
- [ ] Are there any "util" or "helpers" modules that smell like a responsibility that hasn't been named yet?

## 2. Composition Over Inheritance (EDR-002)

- [ ] Is `SiteConfig` still a frozen dataclass with no behavior beyond `__post_init__` validation?
- [ ] Does `Scraper` depend only on `SiteConfig` data, not on any subclass-specific logic?
- [ ] Could you add a third site by creating a new `SiteConfig` instance alone — no code changes to existing modules?
- [ ] Are there any places where you accidentally introduced inheritance where composition would suffice?

## 3. Decorator for Cross-Cutting Concerns (EDR-003)

- [ ] Is `@retry` applied declaratively — does reading the function signature tell you it retries?
- [ ] Does the decorator use `functools.wraps` so debugging and introspection work correctly?
- [ ] Is the retry logic fully testable in isolation (without network, without HTML)?
- [ ] Is `time.sleep` monkeypatched in tests so retry tests run instantly?
- [ ] Does the exception hierarchy (`TransientFetchError`, `PermanentFetchError`) correctly classify every failure mode you've encountered?

## 4. Separation of Concerns (Chapter 4 Principles)

- [ ] Can you swap `requests` for `httpx` by changing only `fetcher.py`?
- [ ] Can you switch from JSON output to SQLite by changing only `storage.py`?
- [ ] Does the CLI layer (`cli.py`) contain zero business logic — only argument parsing and orchestration?
- [ ] Does `scraper.py` orchestrate without knowing HTTP details, parsing details, or storage format?
- [ ] Are there any import cycles between modules?

## 5. Error Handling

- [ ] Does every `except` clause catch the narrowest exception type possible?
- [ ] Are there any bare `except:` or `except Exception:` blocks that swallow errors silently?
- [ ] Does the exception hierarchy cover all failure modes encountered so far?
- [ ] Are transient errors (network timeout, 503) clearly distinguished from permanent errors (404, malformed HTML)?
- [ ] Do error messages include enough context to diagnose the problem (URL, status code, attempt number)?

## 6. Testing

- [ ] Does every module have a corresponding `test_*.py` file?
- [ ] Do tests test behavior (what the function does) rather than implementation (how it does it)?
- [ ] Are tests independent — can each run in isolation without depending on test execution order?
- [ ] Are there tests for the unhappy path (network failure, invalid HTML, missing selectors)?
- [ ] Do retry tests verify both the retry count and the backoff timing (monkeypatched)?
- [ ] Is there at least one integration-style test that runs fetch → parse → store end-to-end?

## 7. Code Hygiene

- [ ] Are there any dead imports, commented-out code blocks, or TODO comments that should be resolved?
- [ ] Is logging used consistently — `logger.info` for operations, `logger.warning` for recoverable issues, `logger.error` for failures?
- [ ] Are function signatures clean — no more than 3–4 parameters without a data container?
- [ ] Do functions return values rather than mutating arguments in place?
- [ ] Is naming consistent across the project? (e.g., `fetch_page` vs. `get_page` — pick one style)

## 8. EDR Audit

- [ ] Re-read EDR-001: Does the current module layout match what was described? If you deviated, update the EDR or create a new one explaining why.
- [ ] Re-read EDR-002: Is composition still the right call? Did you encounter a case where it felt awkward?
- [ ] Re-read EDR-003: Is the decorator still the right mechanism? Did you encounter a case where inline retry would have been simpler?
- [ ] Are there decisions you made during V1–V3 that have no EDR but should? Common candidates:
  - How you structured the CLI entry point
  - How you handle logging configuration
  - Why you chose a particular test organization
  - How you classify HTTP status codes into transient vs. permanent

## 9. Readiness for V4

V4 introduces `typing.Protocol` and dependency injection. Before proceeding:

- [ ] Is `fetcher.py` a clean, self-contained module with a clear interface (function signatures that could become a Protocol)?
- [ ] Does `Scraper` currently import `fetcher` directly, or does it receive fetching behavior as a parameter? (If directly — that's what V4 will change.)
- [ ] Are there any tight couplings between modules that will make Protocol extraction harder?
- [ ] Is the test suite green? (Never add abstraction layers on top of broken tests.)

---

## Actions After Review

For each issue found:

1. **Trivial fix** (dead import, inconsistent name) → fix it now, run tests.
2. **Design question** (wrong module boundary, missing abstraction) → write an EDR documenting the decision, then fix if warranted.
3. **Not broken but noted** → add a comment in this checklist with your reasoning for leaving it as-is.

The goal is to enter Week 05 with clean, well-documented code and zero implicit decisions hiding in the codebase.
