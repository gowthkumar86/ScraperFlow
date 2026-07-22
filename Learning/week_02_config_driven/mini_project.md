# Week 02 Implementation Guide — ScraperFlow V2: Config-Driven Multi-Site

## Objective

Scrape a second, different site without copy-pasting the first script. A `SiteConfig` dataclass separates *what varies* (selectors, site name, URL patterns) from *what stays fixed* (the fetch → parse → store orchestration shape). One `Scraper` class handles any site described by a `SiteConfig` — zero site-specific branching anywhere.

## What Broke (Why This Version Exists)

V1's `parse_article()` has CSS selectors hardcoded for a single site (Books to Scrape). Adding a second site forces the question: is the duplication between two site-specific parsers *essential* (truly the same concept — "extract structured data from HTML using CSS selectors") or *coincidental* (two things that happen to look similar today but will diverge)?

The answer: the **shape** of the work is the same (fetch a page, select elements by CSS, extract text), but the **data** driving that shape (which selectors, which field names) varies per site. That makes this data-shaped variation — a dataclass holding configuration, not a class hierarchy with overridden methods.

## Requirements

1. A `SiteConfig` dataclass that captures everything that varies per site — at minimum: site name, base URL, and a mapping of field names to CSS selectors
2. A `Scraper` class (or function) that accepts a `SiteConfig` and orchestrates fetch → parse → store without knowing which site it's scraping
3. A generic parse function that uses `SiteConfig`'s selectors instead of hardcoded ones
4. Two working `SiteConfig` entries for two real, different websites
5. The V1 site (Books to Scrape) must be one of the two configs — prove backward compatibility
6. Zero site-specific `if/elif` branching in `Scraper` or the generic parser
7. All V1 tests still pass (possibly with minor adaptation to the new interface)
8. `logging` updated to include site name in log messages for multi-site runs

## Architecture Decisions to Make

- **Should `SiteConfig` be frozen (immutable)?** Consider: does anything ever need to modify a config after creation? What does `frozen=True` buy you?
- **Where do `SiteConfig` instances live?** In a Python module? A JSON/YAML file? Hard-code them for now — the handbook explicitly says not to build a config file loader before you need one.
- **Should the parser be a method on `Scraper` or a standalone function that receives config?** Consider: does parsing *need* state beyond the config passed in?
- **What's the right level of selector granularity in `SiteConfig`?** A flat dict of `{field_name: css_selector}`? Nested structure? Decide based on what two real sites actually need — not what you imagine a hypothetical third site might need.
- **Composition vs. inheritance:** Why is `SiteConfig` as a data container passed *into* `Scraper` the right choice over a `BaseScraper` with `BooksScraper(BaseScraper)` and `SiteTwoScraper(BaseScraper)` subclasses? Decide and document in EDR-002.

## Acceptance Criteria

- [ ] Running ScraperFlow with Site A's config produces correct output
- [ ] Running ScraperFlow with Site B's config produces correct output
- [ ] `Scraper` class/function contains zero references to any specific site's selectors or structure
- [ ] `SiteConfig` is a `@dataclass` with appropriate fields, defaults, and (optionally) `frozen=True`
- [ ] Adding a hypothetical third site would require only a new `SiteConfig` instance — no code changes
- [ ] All V1 tests still pass
- [ ] Log messages include the site name being scraped

## Tests to Write

- [ ] `test_scraper_with_site_a_config` — Scraper produces expected output given Site A's config and known HTML
- [ ] `test_scraper_with_site_b_config` — Scraper produces expected output given Site B's config and known HTML
- [ ] `test_scraper_no_site_specific_branching` — verify Scraper class source contains no references to specific site names (a meta-test, or just a manual code review checkpoint)
- [ ] `test_siteconfig_immutability` — if using `frozen=True`, verify that attempting to modify a field raises `FrozenInstanceError`
- [ ] `test_siteconfig_defaults` — verify that optional fields have sensible defaults
- [ ] `test_generic_parser_with_selectors` — given arbitrary HTML and a selector mapping, the generic parser extracts the correct fields

## Refactoring Checkpoint

- [ ] Extract `SiteConfig` from the hardcoded selectors in V1's `parse_article()`
- [ ] Confirm zero behavior change: V1's output for Books to Scrape should be identical before and after the refactor
- [ ] Delete the original site-specific `parse_article()` with hardcoded selectors — don't leave it as dead code "just in case"
- [ ] Centralize any ad hoc error handling left over from V1 (if you added workarounds)

## EDR to Write

**EDR-002: Why Composition Over Inheritance for SiteConfig** — Document why a `SiteConfig` dataclass passed into a generic `Scraper` was chosen over a `BaseScraper` class hierarchy with per-site subclasses. Address: what kind of variation exists (data-shaped vs. behavior-shaped), why inheritance would be a stronger coupling than needed, and when inheritance *would* have been the right call.

## Files to Create / Modify

- `scraperflow/config.py` — `SiteConfig` dataclass definition and site config instances
- `scraperflow/scraper.py` — generic `Scraper` class that accepts `SiteConfig`
- `scraperflow/parser.py` — refactored to accept selectors from config instead of hardcoding them
- `scraperflow/cli.py` — updated to accept a site name or config selection, wire `SiteConfig` into `Scraper`
- `tests/test_scraper.py` — tests for `Scraper` across multiple configs
- `tests/test_config.py` — tests for `SiteConfig` behavior (frozen, defaults, `__post_init__` validation)

## Done When

One `Scraper` class, two working `SiteConfig` entries, zero site-specific branching anywhere. The original site-specific code is deleted, not left as dead code.

## Watch For

- **Reaching for inheritance instead of composition** — this is the exact week that mistake is easiest to make. If you're writing `class BooksScraper(BaseScraper)`, stop and reconsider.
- **Over-engineering `SiteConfig`** — don't add fields for pagination, authentication, or JS rendering yet. Those are real needs that belong in later versions (V4, V7).
- **Building a config file loader (JSON/YAML)** — resist it. Hardcoded Python `SiteConfig` instances are fine for two sites. A file-based config system is a feature you don't need yet.
- **Leaving V1's hardcoded parser around "just in case"** — delete it. If you need it back, that's what version control is for.

## Stretch Goals

- Add `__post_init__` validation to `SiteConfig` (e.g., verify `base_url` starts with `http`)
- Support an optional `description` field on `SiteConfig` for human-readable context
- Add a `--site` CLI flag to select which config to use instead of scraping all sites
