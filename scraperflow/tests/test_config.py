# tests/test_config.py
import pytest
from dataclasses import FrozenInstanceError
from scraperflow.config import SelectorMap, SiteConfig


# --- SiteConfig immutability ---

def test_siteconfig_is_frozen():
    selectors = SelectorMap(title="h1")
    config = SiteConfig(domain="example.com", url="https://example.com", selectors=selectors)
    with pytest.raises(FrozenInstanceError):
        config.domain = "other.com"


def test_selectormap_is_frozen():
    selectors = SelectorMap(title="h1", price=".price")
    with pytest.raises(FrozenInstanceError):
        selectors.title = "h2"


# --- SiteConfig / SelectorMap defaults ---

def test_selectormap_defaults():
    selectors = SelectorMap()
    assert selectors.title is None
    assert selectors.price is None
    assert selectors.description is None
    assert selectors.product_image is None
    assert selectors.category_path is None
    assert selectors.technical_details == {}
    assert selectors.custom_selectors == {}


def test_siteconfig_stores_selectors():
    selectors = SelectorMap(title="h1", price=".cost")
    config = SiteConfig(domain="shop.com", url="https://shop.com/item", selectors=selectors)
    assert config.selectors.title == "h1"
    assert config.selectors.price == ".cost"


# --- default_factory isolation ---

def test_selectormap_default_factory_isolation():
    s1 = SelectorMap()
    s2 = SelectorMap()
    # Each instance gets its own dict — not a shared mutable default
    assert s1.technical_details is not s2.technical_details


# --- SiteConfig requires mandatory fields ---

def test_siteconfig_requires_domain_and_url():
    selectors = SelectorMap(title="h1")
    with pytest.raises(TypeError):
        SiteConfig(selectors=selectors)  # type: ignore[call-arg]