# EDR-002: Why Composition Over Inheritance for SiteConfig

## Status
Accepted

## Problem
ScraperFlow V2 needs to support multiple sites. How should site-specific variation (CSS selectors, domain name, URL patterns) be represented — through a class hierarchy with per-site subclasses, or through a data container (dataclass) passed into a generic scraper?

## Context
V1 has a single `parse_article()` function with hardcoded CSS selectors for Books to Scrape. V2 adds a second site. The variation between sites is purely **data-shaped**: different CSS selectors, different field names, different base URLs. The *behavior* — fetch a page, select elements by CSS, extract text, store results — is identical across sites.

Two canonical approaches exist:

- **Inheritance:** `BaseScraper` defines the algorithm; `BooksScraper(BaseScraper)` and `CarScraper(BaseScraper)` override selector attributes or parsing steps.
- **Composition:** A `SiteConfig` dataclass holds what varies; a single `Scraper` class accepts any `SiteConfig` and executes the fixed algorithm against it.

## Possible Solutions
1. **Inheritance hierarchy** — `BaseScraper` with abstract methods/selectors, one subclass per site.
2. **Composition with a data container** — `SiteConfig` dataclass injected into a generic `Scraper`.
3. **Dictionary/JSON config** — site variation stored in raw dicts or config files, no typed structure.

## Chosen Solution
Option 2 — composition with a `SiteConfig` frozen dataclass.

## Why This Solution Was Selected
- **The variation is data, not behavior.** Each site differs only in *which CSS selectors* to use and *which URL* to fetch — not in *how* to fetch, parse, or store. When variation is data-shaped, a data container is the minimal, correct tool. Inheritance is designed for behavioral polymorphism — using it here adds coupling without benefit.
- **Adding a new site costs one object, not one class.** With composition, supporting site C means creating one new `SiteConfig` instance — zero code changes to `Scraper` or `parser.py`. With inheritance, it means a new file, a new class, and potentially overridden methods that duplicate the parent's logic with trivial differences.
- **Tighter adherence to Open/Closed Principle.** The system is open for extension (new configs) and closed for modification (no edits to existing classes). Inheritance hierarchies tend to require modifications to the base class as edge cases accumulate.
- **Simpler testing.** Tests construct arbitrary `SiteConfig` instances with synthetic HTML — no subclass instantiation, no mocking of overridden methods.
- **`frozen=True` guarantees immutability.** Configs cannot be accidentally mutated mid-run, eliminating an entire class of bugs that mutable base-class attributes would allow.

## Trade-offs Accepted
- If a future site requires genuinely different *behavior* (e.g., JavaScript rendering, pagination, authentication flows), `SiteConfig` alone won't capture it — a behavioral extension point (Protocol/adapter, introduced in V4) will be needed. This is acceptable because V2 explicitly defers those concerns.
- Type annotations on `SelectorMap` fields default to `None`, meaning the parser must guard against missing selectors at runtime rather than getting compile-time guarantees for mandatory fields.

## Why Alternatives Were Rejected
- **Option 1 (inheritance):** Coupling is stronger than needed. Each subclass is tightly bound to the base class's interface; changes to the parsing algorithm require touching every subclass. Additionally, the Rule of Three hasn't been met — two sites don't justify an abstract hierarchy.
- **Option 3 (raw dicts):** Loses type safety, IDE support, and `frozen` immutability. Typos in selector keys become silent bugs instead of attribute errors.

## When Inheritance *Would* Be the Right Call
- When sites require **different algorithms**, not just different data (e.g., one site needs browser rendering while another needs only HTTP — addressed in V4 via Protocol).
- When the Template Method pattern genuinely applies: a fixed sequence of steps where subclasses override individual steps with meaningfully different logic.

## When to Revisit
- If a third or fourth site introduces variation that cannot be expressed as selector strings (e.g., multi-page crawling, login flows), consider whether the variation is still data-shaped or has become behavioral — and reach for Protocol-based adapters (V4) rather than inheritance.