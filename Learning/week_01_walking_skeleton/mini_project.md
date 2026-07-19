# Week 01 Implementation Guide — ScraperFlow V1: Walking Skeleton

## Objective

Build the absolute minimal end-to-end scraper: one CLI command fetches a list of URLs, parses HTML to extract structured data, and writes results to `output.json`. Every architectural seam (fetch / parse / store) exists as a real function boundary, even though each piece is trivial. This is a walking skeleton — its job is to convert guesses about "how ScraperFlow should work" into observed facts, cheaply, before any structure gets built around assumptions instead of evidence.

## What Broke (Why This Version Exists)

Nothing broke — this is the starting point. There is nothing to build on yet. The walking skeleton exists so that later versions have real function boundaries to attach to, instead of carving seams out of a monolith after the fact.

## Requirements

1. A `scraperflow/` package with at minimum: `fetcher.py`, `parser.py`, `storage.py`, `cli.py`
2. `fetch_page(url: str) -> str` — uses `requests`, returns raw HTML, raises on non-2xx status
3. `parse_article(html: str, ...) -> dict` — uses BeautifulSoup, extracts structured data using CSS selectors
4. `save_records(records: list[dict], output_path: str) -> None` — writes to JSON file
5. CLI via `argparse` accepts a list of URLs (or a file containing URLs) and an output path
6. `logging` used throughout (not `print`) — at minimum `INFO` for start/complete, `WARNING` for skipped URLs, `ERROR` for failures
7. Deliberate failure policy: log and skip failed URLs, don't crash the entire run
8. Output is valid JSON — a list of record dicts

## Architecture Decisions to Make

- How to organize modules: one file per responsibility (fetch/parse/store) or fewer files? Decide based on separation of concerns, not current size.
- What constitutes a "record"? Decide on a minimal dict shape (e.g., `{"url": ..., "title": ..., "content": ...}`) — this becomes the contract between parse and store.
- Where does orchestration live? The CLI wires things together, but should there be a `run()` or `scrape()` function that sequences fetch→parse→store?
- What's the failure policy? "Log and skip" is the deliberate V1 choice. Document it as a named policy, not an accident.

## Acceptance Criteria

- [ ] Running `python -m scraperflow --urls <url1> <url2> --output output.json` produces a valid JSON file
- [ ] Each URL becomes one record in the output (or is logged as skipped on failure)
- [ ] The code is organized into separate modules by responsibility
- [ ] `logging` is used instead of `print` throughout
- [ ] At least two passing `pytest` tests exist on the parsing function
- [ ] The output JSON is valid and contains expected fields
- [ ] Failed URLs produce a log warning, not a crash

## Tests to Write

- [ ] `test_parse_article_extracts_title` — given a known HTML string, parser returns expected title
- [ ] `test_parse_article_extracts_content` — given a known HTML string, parser returns expected content field(s)
- [ ] `test_parse_article_handles_missing_element` — parser returns `None` or empty for missing selectors, doesn't crash
- [ ] `test_save_records_creates_valid_json` — given a list of dicts, output file contains valid JSON matching input
- [ ] `test_save_records_overwrites_existing_file` — verify behavior when output file already exists

## Refactoring Checkpoint

- None for V1. This is the starting point.

## EDR to Write

- **EDR-001: Module Layout and Responsibility Boundaries** — Why `fetcher.py` / `parser.py` / `storage.py` as separate modules even when each is small. Document the "organize by responsibility at effectively zero cost" reasoning.

## Files to Create / Modify

- `scraperflow/__init__.py` — package marker
- `scraperflow/fetcher.py` — `fetch_page()` function
- `scraperflow/parser.py` — `parse_article()` function
- `scraperflow/storage.py` — `save_records()` function
- `scraperflow/cli.py` — `argparse` setup, orchestration
- `scraperflow/__main__.py` — enables `python -m scraperflow`
- `tests/__init__.py` — test package marker
- `tests/test_parser.py` — parsing tests against HTML fixtures
- `tests/test_storage.py` — storage tests
- `output.json` — generated output (gitignored)

## Done When

One CLI command produces a valid `output.json` from real URLs, at least two passing tests exist on the parsing function, and the first commit is clean, not a dump.

## Watch For

- The urge to add config beyond CLI args — resist it, that's Week 2
- Splitting into more modules than fetch/parse/storage — not needed yet
- Adding retry logic or error handling beyond "log and skip" — that's Week 3
- Over-engineering the record shape — a flat dict is fine for V1

## Stretch Goals

- Add a `--verbose` flag that sets logging to `DEBUG`
- Support reading URLs from a file (`--url-file urls.txt`)
- Add a `--format` flag (json/jsonl) — but don't build a storage abstraction yet
