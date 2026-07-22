# Week 02: Config-Driven Multi-Site — ScraperFlow V2

**Prerequisites confirmed solid:** Python fundamentals, modules & packages, `logging`, `argparse`, `requests`, `BeautifulSoup`, `json`, `pytest` basics, separation of concerns, walking skeleton pattern
**Prerequisites assumed but not confirmed:** comfort with CSS selectors across different site structures, browser DevTools inspection workflow

## Overview

This week transforms ScraperFlow from a single-site scraper into a config-driven, multi-site system. Instead of hardcoded selectors in `parser.py`, a `SiteConfig` dataclass captures *what varies* per site (selectors, site name, base URL) while a generic `Scraper` class owns *what stays fixed* (the fetch → parse → store shape). The key insight: the variation between sites is **data-shaped** (different CSS selectors, different field names), not **behavior-shaped** — so composition with a data container is the right tool, not inheritance.

## Learning Objectives

- [ ] Understand and use `@dataclass` — fields, defaults, `frozen`, `__post_init__`
- [ ] Apply composition over inheritance when variation is data-shaped
- [ ] Distinguish essential duplication from coincidental duplication
- [ ] Understand configuration as data vs. configuration as code
- [ ] Know the Rule of Three and when acting before three cases is justified
- [ ] Inspect a new site's structure using browser DevTools
- [ ] Design a `SiteConfig` that captures what varies without over-specifying

## Concepts Covered

| Discipline | Concepts |
|---|---|
| Python | `@dataclass` (fields, defaults, `frozen`, `__post_init__`), composition over inheritance |
| Architecture | configuration as data vs. code, essential vs. coincidental duplication, Rule of Three |
| Skills | DevTools site inspection, designing `SiteConfig` |
| Testing | testing `Scraper` across multiple `SiteConfig` entries |

## ScraperFlow Version

- **Version:** V2
- **Milestone:** `v0.2 — Multi-Site`
- **Depends on:** V1 (Walking Skeleton)

## Official References

- [Python `dataclasses` module](https://docs.python.org/3/library/dataclasses.html)
- [PEP 557 — Data Classes](https://peps.python.org/pep-0557/)
- [Python `dataclasses.field()`](https://docs.python.org/3/library/dataclasses.html#dataclasses.field)
- [Martin Fowler — Rule of Three](https://martinfowler.com/bliki/RuleOfThree.html)
- [PyCon talk: "Stop Writing Classes" (Jack Diederich)](https://www.youtube.com/watch?v=o9pEzgHorH0)
- [Chrome DevTools documentation](https://developer.chrome.com/docs/devtools/)

## Learning Checklist

- [ ] Read `notes.ipynb` — all discipline sections
- [ ] Complete `practice.py` exercises
- [ ] Implement ScraperFlow V2 following `mini_project.md`
- [ ] Write tests listed in `mini_project.md`
- [ ] Complete refactoring checkpoint: extract `SiteConfig`, confirm zero behavior change
- [ ] Write EDR-002: Why Composition Over Inheritance for SiteConfig
- [ ] All prior tests still pass
- [ ] Original site-specific code is deleted, not left as dead code

## Additional Resources

- *Fluent Python* by Ramalho — Chapter on data classes and class builders
- *Architecture Patterns with Python* (Percival & Gregory) — cosmicpython.com — composition and dependency injection patterns
- Martin Fowler's blog (martinfowler.com) — Rule of Three, essential vs. coincidental duplication
- PyCon talk: "Stop Writing Classes" (Jack Diederich) — the composition-over-inheritance argument, made sharply
