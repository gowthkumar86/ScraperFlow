# tests/test_parser.py
import pytest
from pathlib import Path
from scraperflow.parser import parse_article
from scraperflow.config import SelectorMap, SiteConfig


@pytest.fixture
def books_config():
    selectors = SelectorMap(
        title=".col-sm-6.product_main h1",
        price=".col-sm-6.product_main .price_color",
        description=".product_page>p",
        product_image=".thumbnail img",
    )
    return SiteConfig(domain="bookstoscrape.com", url="https://books.toscrape.com", selectors=selectors)


@pytest.fixture
def html_source():
    path = Path(__file__).parent.parent / "html_source.html"
    return path.read_text(encoding="utf-8")


def test_parse_article_extracts_title(html_source, books_config):
    result = parse_article(html_source, "http://example.com/book", books_config)
    assert result["title"] == "A Light in the Attic"


def test_parse_article_extracts_price(html_source, books_config):
    result = parse_article(html_source, "http://example.com/book", books_config)
    assert result["price"] == "£51.77"


def test_parse_article_extracts_description(html_source, books_config):
    result = parse_article(html_source, "http://example.com/book", books_config)
    assert result["description"] is not None
    assert "A Light in the Attic" in result["description"]


def test_parse_article_handles_missing_element(books_config):
    html = "<html><body><p>No product here</p></body></html>"
    result = parse_article(html, "http://example.com/empty", books_config)
    assert result is None