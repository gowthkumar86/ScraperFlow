# Week 01: Walking Skeleton — ScraperFlow V1

**Prerequisites confirmed solid:** Python fundamentals (functions, modules, classes, exceptions, venvs), SQL basics, web scraping experience (requests, BeautifulSoup, HTTP concepts)
**Prerequisites assumed but not confirmed:** pytest familiarity, logging module usage, argparse usage

## Overview

This week builds the absolute minimal version of ScraperFlow: a CLI command that fetches URLs, parses HTML, and writes structured data to a JSON file. Every seam (fetch/parse/store) exists as a real function boundary from day one — not because it's complex, but so later versions have something to attach to instead of carving boundaries out of a monolith after the fact.

This is a **walking skeleton** — every architectural boundary exists, even though each piece is trivial.

## Learning Objectives

- [ ] Understand and apply Python module/package organization by responsibility
- [ ] Use `logging` correctly (levels, handlers, formatters) instead of `print`
- [ ] Build a CLI with `argparse` to separate data from code
- [ ] Fetch web pages with `requests` and handle HTTP basics (status codes, headers)
- [ ] Parse HTML with `BeautifulSoup` using CSS selectors
- [ ] Serialize structured data with `json`
- [ ] Write first `pytest` tests — assertions, fixtures, test discovery
- [ ] Apply separation of concerns at the function level
- [ ] Understand the walking skeleton pattern and why it matters

## Concepts Covered

| Discipline | Concepts |
|---|---|
| Python | modules & packages, `logging` (levels, handlers, formatters), `argparse`, `requests`, `BeautifulSoup`, `json` serialization, `pytest` basics (assertions, fixtures, test discovery) |
| Architecture | separation of concerns (at function level), walking skeleton pattern |
| Testing | pure-function testing, test discovery, fixtures, assertions |
| Skills | HTTP fundamentals (status codes, headers), HTML parsing, CSS selectors, writing clean first commits |

## ScraperFlow Version

- **Version:** V1
- **Milestone:** `v0.1 — Walking Skeleton`
- **Depends on:** Nothing — this is the foundation

## Official References

- [Python `logging` module](https://docs.python.org/3/library/logging.html)
- [Python `logging` HOWTO](https://docs.python.org/3/howto/logging.html)
- [Python `argparse` tutorial](https://docs.python.org/3/howto/argparse.html)
- [Requests documentation](https://requests.readthedocs.io/en/latest/)
- [BeautifulSoup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Python `json` module](https://docs.python.org/3/library/json.html)
- [pytest documentation](https://docs.pytest.org/en/stable/)
- [HTTP Status Codes (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

## Learning Checklist

- [ ] Read `notes.ipynb` — all discipline sections
- [ ] Complete `practice.py` exercises
- [ ] Implement ScraperFlow V1 following `mini_project.md`
- [ ] Write tests listed in `mini_project.md`
- [ ] Complete refactoring checkpoint (N/A for V1 — this is the starting point)
- [ ] Write EDR-001: Module Layout and Responsibility Boundaries
- [ ] All prior tests still pass (N/A for V1 — no prior tests exist)
- [ ] First commit is clean, not a dump

## Additional Resources

- *Effective Python* by Brett Slatkin — Items on logging and module organization
- *Python Testing with pytest* by Brian Okken — Chapters 1–2
- [Real Python: Logging in Python](https://realpython.com/python-logging/)
- [Real Python: Beautiful Soup Web Scraping](https://realpython.com/beautiful-soup-web-scraper-python/)
