# tests/test_parser.py
import pytest
from pathlib import Path
from scraperflow.parser import parse_article


@pytest.fixture
def html_source():
    path = Path(__file__).parent.parent / "html_source.html"
    return path.read_text(encoding="utf-8")


def test_parse_article_extracts_title(html_source):
    result = parse_article(html_source, "http://example.com/book")
    assert result["title"] == "A Light in the Attic"


def test_parse_article_extracts_price(html_source):
    result = parse_article(html_source, "http://example.com/book")
    assert result["price"] == "£51.77"


def test_parse_article_extracts_rating(html_source):
    result = parse_article(html_source, "http://example.com/book")
    assert result["rating"] == "Three"


def test_parse_article_extracts_description(html_source):
    result = parse_article(html_source, "http://example.com/book")
    assert result["description"] is not None
    assert "A Light in the Attic" in result["description"]


def test_parse_article_handles_missing_element():
    html = "<html><body><p>No product here</p></body></html>"
    result = parse_article(html, "http://example.com/empty")
    assert result is None