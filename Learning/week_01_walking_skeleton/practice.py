"""
Week 01: Walking Skeleton
ScraperFlow Version: V1
Concepts: modules & packages, logging (levels, handlers, formatters), argparse,
          requests, BeautifulSoup, json serialization, pytest (assertions, fixtures,
          test discovery), separation of concerns, HTTP fundamentals
"""

# --- Python Concepts: logging ---

# Exercise 1: Basic logging setup
# Create a logger named "scraper" with:
# - A StreamHandler that outputs to stdout
# - A Formatter that includes: timestamp, logger name, level, and message
# - Set the level to INFO
# Log one message at each level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# and verify only INFO and above appear.
import logging
import sys

logger = logging.getLogger("scraper")
logger.setLevel(logging.DEBUG)

# StreamHandler
console_handler = logging.StreamHandler(sys.stdout)

format = logging.Formatter("%(asctime)s | %(name)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(format)
console_handler.setLevel(logging.INFO)

logger.addHandler(console_handler)

print("="*50+"Exercise 1","="*50)
#log
logger.debug("DEBUG THIS FILE")
logger.info("This is INFO")
logger.warning("This is warning")
logger.error("This is error")

# Exercise 2: Logging to a file
# Configure the same logger to ALSO write to a file "scraper.log"
# with a different format (include filename and line number).
# Demonstrate that both handlers receive messages independently.
file_handler = logging.FileHandler("scraper.log", mode="a")
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    "%(asctime)s | %(name)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s"
)

file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)

print("="*50+"Exercise 2","="*50)
logger.debug("DEBUG THIS FILE")
logger.info("This is INFO")
logger.warning("This is warning")
logger.error("This is error")





# --- Python Concepts: argparse ---

# Exercise 3: CLI argument parsing
# Write a function `build_parser()` that returns an ArgumentParser with:
# - A required positional argument "urls" (nargs="+")
# - An optional argument "--output" with default "output.json"
# - An optional flag "--verbose" that stores True
# Parse the args: ["http://example.com", "http://test.com", "--output", "data.json"]
# and verify the namespace has the expected values.
import argparse

def build_parser():
    
    parser = argparse.ArgumentParser(description= "ScraperFlow V1 : Fetch, Parse, Store results")

    parser.add_argument(
        "urls",
        nargs="+",
        help= "One or more urls to scrape",  
    )

    parser.add_argument(
        "--output",
        default="output.json",
        help="Output file path"
    )

    parser.add_argument(
        "--verbose","--v",
        action= "store_true",
        help= "Enable verbose (DEBUG) logging"
    )

    return parser

parser = build_parser()
args = parser.parse_args(["http://example.com", "http://test.com"])


print("="*50+"Exercise 3","="*50)
print(f"URLs: {args.urls}")
print(f"Output: {args.output}")
print(f"Verbose: {args.verbose}")



# --- Python Concepts: requests & HTTP ---

# Exercise 4: Status code handling
# Write a function `check_response(status_code: int) -> str` that returns:
# - "success" for 2xx codes
# - "redirect" for 3xx codes
# - "client_error" for 4xx codes
# - "server_error" for 5xx codes
# Do NOT use requests here — just the status code integer.
def classify_status(status_code: int) -> str:
    """Classify HTTP status code into category."""
    if 200 <= status_code < 300:
        return "success"
    elif 300 <= status_code < 400:
        return "redirect"
    elif 400 <= status_code < 500:
        return "client_error"
    elif 500 <= status_code < 600:
        return "server_error"
    else:
        return "unknown"

# Verify
print("="*50+"Exercise 4","="*50)
assert classify_status(200) == "success"
assert classify_status(301) == "redirect"
assert classify_status(404) == "client_error"
assert classify_status(500) == "server_error"
print("All status code classifications correct")

# Exercise 5: Headers
# Write a function `build_headers(user_agent: str, accept: str) -> dict`
# that returns a properly structured headers dict for use with requests.
# Include "User-Agent", "Accept", and "Accept-Language" (hardcode to "en-US").
def build_headers(user_agent: str, accept: str) -> dict:
    return {
        "User-Agent": user_agent,
        "Accept": accept,
        "Accept-Language": "en-US"
    }

print("="*50+"Exercise 5","="*50)
headers = build_headers(
    user_agent="Mozilla/5.0",
    accept="application/json"
)

print(headers)

# --- Python Concepts: BeautifulSoup & CSS Selectors ---

# Exercise 6: Parsing HTML
# Given the following HTML string:
HTML_SAMPLE = """
<html>
<head><title>Test Article</title></head>
<body>
  <article>
    <h1 class="title">Breaking News</h1>
    <p class="author">Jane Doe</p>
    <div class="content">
      <p>First paragraph of the article.</p>
      <p>Second paragraph of the article.</p>
    </div>
    <span class="date">2024-01-15</span>
  </article>
</body>
</html>
"""
# Write a function `extract_article(html: str) -> dict` that returns:
# {"title": "Breaking News", "author": "Jane Doe",
#  "content": "First paragraph...\nSecond paragraph...", "date": "2024-01-15"}
from bs4 import BeautifulSoup
def extract_article(html: str) -> dict:
    """Extract structured data from an article HTML page."""
    soup = BeautifulSoup(html, "html.parser")
    
    title_el = soup.select_one("h1.title")
    author_el = soup.select_one(".author")
    content_els = soup.select("div.content p")
    date_el = soup.select_one(".date")
    
    return {
        "title": title_el.get_text() if title_el else None,
        "author": author_el.get_text() if author_el else None,
        "content": "\n".join(p.get_text() for p in content_els) if content_els else None,
        "date": date_el.get_text() if date_el else None,
    }

result = extract_article(HTML_SAMPLE)

print("="*50+"Exercise 6","="*50)
print(result)

# Exercise 7: Handling missing elements
# Write a function `safe_extract(html: str, selector: str) -> str | None`
# that returns the text of the first element matching the CSS selector,
# or None if no element matches. Should never raise an exception.
def safe_extract(html: str, selector: str) -> str | None:
    """Safely extract text from first element matching selector, or None."""
    soup = BeautifulSoup(html, "html.parser")
    element = soup.select_one(selector)
    return element.get_text(strip=True) if element else None

# Works when element exists
assert safe_extract(HTML_SAMPLE, "h1.title") == "Breaking News"

# Returns None when element is missing (no exception)
assert safe_extract(HTML_SAMPLE, "h2.subtitle") is None

print("="*50+"Exercise 7","="*50)
print("safe_extract works correctly")


# --- Python Concepts: json serialization ---

# Exercise 8: JSON round-trip
# Write two functions:
# - `serialize_records(records: list[dict]) -> str` — returns a JSON string
#   with indent=2 and ensure_ascii=False
# - `deserialize_records(json_str: str) -> list[dict]` — parses it back
# Verify that round-tripping preserves the data exactly.



# Exercise 9: Handling non-serializable types
# Write a function `make_serializable(record: dict) -> dict` that converts:
# - datetime objects to ISO format strings
# - sets to sorted lists
# - bytes to UTF-8 decoded strings
# Return a new dict (don't mutate the input).



# --- Python Concepts: pytest ---

# Exercise 10: Writing a fixture
# Write a pytest fixture called `sample_html` that returns the HTML_SAMPLE
# string above. Then write a test function `test_title_extraction` that
# uses this fixture and asserts the title is "Breaking News".
# (Write just the function signatures and docstrings — don't implement)


# --- Architecture / Design Exercises ---

# Exercise 11: Separation of concerns
# Below is a single function that does everything. Refactor it into three
# separate functions (fetch, parse, save) with clear interfaces between them.
# Only write the function signatures and docstrings — not the implementation.

def scrape_and_save(url, output_file):
    """This function fetches a URL, extracts the title and first paragraph,
    and writes them to a JSON file. It does too much."""
    pass  # Imagine this has 40 lines of mixed concerns


# Exercise 12: Function contracts
# For each of these three functions, write the type signature and a one-line
# docstring describing its SINGLE responsibility:
# - The fetcher (input? output? what can go wrong?)
# - The parser (input? output? what can go wrong?)
# - The storage writer (input? output? what can go wrong?)


# --- Challenge ---

# Challenge: Mini pipeline orchestrator
# Write a function `run_pipeline(urls: list[str]) -> list[dict]` that:
# 1. Iterates over URLs
# 2. Calls a `fetch` function (you define the signature)
# 3. Calls a `parse` function on the result
# 4. Collects successfully parsed records into a list
# 5. Logs (using logging, not print) each step: fetching, parsing, success/failure
# 6. On ANY exception during fetch or parse for a single URL: logs a WARNING
#    and continues to the next URL (doesn't crash the whole run)
# 7. Returns the list of successfully parsed records
#
# Requirements:
# - Use logging, not print
# - The failure policy is "log and skip" — deliberate, not accidental
# - Each function (fetch/parse) should have a clear single responsibility
# - Type hints on all function signatures
#
# Do NOT actually make network calls — use placeholder implementations
# that demonstrate the STRUCTURE, not the I/O.
