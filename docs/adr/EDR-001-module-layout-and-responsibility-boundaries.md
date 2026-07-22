# EDR-001: Module Layout and Responsibility Boundaries

## Status
Accepted

## Problem
ScraperFlow V1 is small enough to fit in a single script. Should the code live in one file, or be split into separate modules by responsibility — even when each module contains only one function?

## Context
V1 has three distinct responsibilities: fetching HTML over HTTP, parsing HTML into structured data, and persisting records to a file. Each is currently ~10–20 lines. A single `scraper.py` would work today with less boilerplate (no `__init__.py`, no cross-module imports).

## Possible Solutions
1. **One script** — `scraper.py` with `fetch_page()`, `parse_article()`, `save_records()` all in one file.
2. **Separate modules by responsibility** — `fetcher.py`, `parser.py`, `storage.py`, `cli.py` inside a `scraperflow/` package.
3. **Split later** — start with option 1, refactor when it "gets big enough."

## Chosen Solution
Option 2 — separate modules from day one.

## Why This Solution Was Selected
- **Organizing by responsibility costs effectively nothing.** Four small files with clear names are no harder to navigate than one longer file — arguably easier, since the file name tells you where to look.
- **It's not premature abstraction.** No interfaces, no inheritance, no frameworks — just putting functions that change for different reasons into different files. The three responsibilities (fetch, parse, store) change independently: switching from `requests` to `httpx` touches only `fetcher.py`; changing CSS selectors touches only `parser.py`; switching from JSON to SQLite touches only `storage.py`.
- **Later versions attach to these seams.** V3 adds retry logic around fetching, V4 abstracts the engine behind a Protocol, V6 abstracts storage. Each of those changes is scoped to one module because the boundary already exists — no extraction refactor needed first.
- **Option 3 ("split later") has a hidden cost.** By the time a single file feels big enough to split, imports, test files, and habits have formed around the monolithic shape. Splitting retroactively means updating every import, moving tests, and re-learning where things live — work that's free to avoid by starting split.

## Trade-offs Accepted
- Slightly more boilerplate (package `__init__.py`, cross-module imports) for a project that currently has ~50 lines of logic.
- A new contributor seeing four near-empty files might wonder if the project is over-engineered — the README and this EDR explain why it isn't.

## Why Alternatives Were Rejected
- **Option 1** saves ~2 minutes of setup today and costs real refactoring effort the moment any single responsibility needs to change independently (which V2 already requires).
- **Option 3** optimizes for "feels necessary" over "costs nothing now and saves work later" — the exact junior-engineer trade-off Chapter 2 warns against.

## When to Revisit
If a module grows large enough to warrant further splitting (e.g., `parser.py` handling multiple parsing strategies), split by sub-responsibility at that point — same principle, applied recursively.