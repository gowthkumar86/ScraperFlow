# Week 03: Retry & Resilience — ScraperFlow V3

**Prerequisites confirmed solid:** `@dataclass`, composition over inheritance, configuration as data, `SiteConfig` design, separation of concerns, `pytest` basics
**Prerequisites assumed but not confirmed:** comfort with closures (inner functions capturing outer scope), basic exception handling (`try/except/raise`)

## Overview

This week adds resilience to ScraperFlow. Running V2 against real sites surfaces genuine, repeated network failures — timeouts, 5xx responses, connection resets. V3 introduces a small exception hierarchy (`TransientFetchError` vs. `PermanentFetchError`) that classifies failure by type, and a `@retry` decorator that catches narrowly — only failures actually worth retrying — with exponential backoff plus jitter so retries don't hammer an already-struggling server or synchronize into a "thundering herd."

The key architectural insight: retry logic is a **cross-cutting concern** — it applies uniformly across many otherwise-unrelated components and therefore belongs in exactly one place, applied consistently as a decorator, not duplicated inside each function's business logic.

## Learning Objectives

- [ ] Understand decorators deeply — closures, function wrapping, control flow injection
- [ ] Use `functools.wraps` correctly and understand what metadata it preserves
- [ ] Build decorator factories (decorators that accept parameters)
- [ ] Design custom exception hierarchies with intentional catch semantics
- [ ] Distinguish transient from permanent failures and encode that distinction in types
- [ ] Understand cross-cutting concerns and why decorators are the right tool for them
- [ ] Implement exponential backoff with jitter (full-jitter formula)
- [ ] Test retry behavior without real delays using monkeypatching

## Concepts Covered

| Discipline | Concepts |
|---|---|
| Python | Decorators (function decorators, `functools.wraps`, decorator factories, closures), custom exception hierarchies |
| Architecture | Cross-cutting concerns, exponential backoff with jitter, transient vs. permanent failure classification |
| Testing | Monkeypatching `time.sleep`, testing retry behavior without real delays |

## ScraperFlow Version

- **Version:** V3
- **Milestone:** `v0.3 — Resilient Fetching`
- **Depends on:** V2 (Config-Driven Multi-Site)

## Official References

- [Python Decorators — Real Python](https://realpython.com/primer-on-python-decorators/)
- [PEP 318 — Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
- [`functools.wraps` documentation](https://docs.python.org/3/library/functools.html#functools.wraps)
- [Python Exception Hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)
- [Exponential Backoff and Jitter — AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [Scrapy RetryMiddleware source](https://github.com/scrapy/scrapy/blob/master/scrapy/downloadermiddlewares/retry.py)
- *Fluent Python* (Ramalho) — Chapters on closures and decorators

## Learning Checklist

- [ ] Read `notes.ipynb` — all discipline sections
- [ ] Complete `practice.py` exercises
- [ ] Implement ScraperFlow V3 following `mini_project.md`
- [ ] Write tests listed in `mini_project.md`
- [ ] Complete refactoring checkpoint: centralize any ad hoc error handling from V1/V2
- [ ] Write EDR-003: Why a decorator for retry instead of inline try/except
- [ ] All prior tests still pass
- [ ] Test suite still runs in well under a second despite testing multi-attempt logic

## Additional Resources

- *Fluent Python* (Ramalho) — decorators chapter covers closures and the decorator pattern in depth
- Scrapy source code — read `RetryMiddleware` for a mature production implementation of the same concept
- `tenacity` library documentation — the production-grade alternative to a hand-rolled retry decorator (understand why we're building our own: learning value)
