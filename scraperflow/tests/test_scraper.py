# tests/test_scraper.py
"""
Tests that the Scraper + parser pipeline works generically across different SiteConfigs.
Uses known HTML fixtures — no network calls.
"""
import pytest
from scraperflow.parser import parse_article
from scraperflow.config import SelectorMap, SiteConfig


# --- Fixtures: two different site configs with matching HTML ---

BOOKS_HTML = """
<html><body>
<div class="col-sm-6 product_main">
  <h1>A Light in the Attic</h1>
  <p class="price_color">£51.77</p>
</div>
<div class="product_page"><p>A great book about living.</p></div>
<div class="thumbnail"><img src="/images/book.jpg"/></div>
</body></html>
"""

CAR_HTML = """
<html><body>
<h1 class="product-title">Mercedes-Benz W123</h1>
<span class="price">$12,500</span>
<p class="description">Classic German sedan from the 1980s.</p>
<div class="gallery"><img src="/images/car.jpg"/></div>
</body></html>
"""


@pytest.fixture
def books_config():
    selectors = SelectorMap(
        title=".col-sm-6.product_main h1",
        price=".col-sm-6.product_main .price_color",
        description=".product_page > p",
        product_image=".thumbnail img",
    )
    return SiteConfig(domain="bookstoscrape.com", url="https://books.toscrape.com", selectors=selectors)


@pytest.fixture
def car_config():
    selectors = SelectorMap(
        title="h1.product-title",
        price=".price",
        description="p.description",
        product_image=".gallery img",
    )
    return SiteConfig(domain="cars.example.com", url="https://cars.example.com", selectors=selectors)


# --- Tests: Scraper with Site A (Books) ---

def test_scraper_with_books_config(books_config):
    result = parse_article(BOOKS_HTML, "https://books.toscrape.com/book/1", books_config)
    assert result is not None
    assert result["title"] == "A Light in the Attic"
    assert result["price"] == "£51.77"
    assert result["description"] == "A great book about living."
    assert result["product_image"] == "/images/book.jpg"
    assert result["url"] == "https://books.toscrape.com/book/1"


# --- Tests: Scraper with Site B (Cars) ---

def test_scraper_with_car_config(car_config):
    result = parse_article(CAR_HTML, "https://cars.example.com/car/1", car_config)
    assert result is not None
    assert result["title"] == "Mercedes-Benz W123"
    assert result["price"] == "$12,500"
    assert result["description"] == "Classic German sedan from the 1980s."
    assert result["product_image"] == "/images/car.jpg"


# --- Tests: generic parser with arbitrary selectors ---

def test_generic_parser_with_selectors():
    """Given arbitrary HTML and a selector mapping, the parser extracts correct fields."""
    html = '<html><body><h2 class="name">Widget</h2><span class="cost">$9.99</span></body></html>'
    selectors = SelectorMap(title="h2.name", price="span.cost")
    config = SiteConfig(domain="widgets.io", url="https://widgets.io", selectors=selectors)

    result = parse_article(html, "https://widgets.io/widget/1", config)
    assert result["title"] == "Widget"
    assert result["price"] == "$9.99"
    assert result["description"] is None
    assert result["product_image"] is None


# --- Tests: no site-specific branching ---

def test_scraper_no_site_specific_branching():
    """Verify Scraper class source contains no references to specific site names."""
    import inspect
    from scraperflow.scraper import Scraper

    source = inspect.getsource(Scraper)
    site_names = ["books", "toscrape", "car", "mercedes", "webscraper.io"]
    for name in site_names:
        assert name.lower() not in source.lower(), (
            f"Scraper source should not reference site-specific string '{name}'"
        )


# --- Tests: parser returns None for missing title ---

def test_parser_returns_none_when_title_not_found():
    html = "<html><body><p>No matching elements</p></body></html>"
    selectors = SelectorMap(title="h1.nonexistent", price=".price")
    config = SiteConfig(domain="empty.com", url="https://empty.com", selectors=selectors)

    result = parse_article(html, "https://empty.com/page", config)
    assert result is None