from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


def parse_article(html: str, url: str, config) -> dict | None:
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.select_one(config.selectors.title)
    price_tag = soup.select_one(config.selectors.price) if config.selectors.price else None
    description_tag = soup.select_one(config.selectors.description) if config.selectors.description else None
    image_tag = soup.select_one(config.selectors.product_image) if config.selectors.product_image else None

    if not title_tag:
        logger.warning(f"Could not parse title from {url}")
        return None

    return {
        "url": url,
        "title": title_tag.get_text(strip=True),
        "price": price_tag.get_text(strip=True).replace("Â","") if price_tag else None,
        "description": description_tag.get_text(strip=True) if description_tag else None,
        "product_image" : image_tag.get('src') if image_tag else None
    }

