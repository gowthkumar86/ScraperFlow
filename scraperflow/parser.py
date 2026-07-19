from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


def parse_article(html: str, url: str) -> dict | None:
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.select_one(".product_main h1")
    price_tag = soup.select_one(".price_color")
    availability_tag = soup.select_one(".availability")
    rating_tag = soup.select_one(".star-rating")
    description_tag = soup.select_one("#product_description ~ p")

    if not title_tag:
        logger.warning(f"Could not parse title from {url}")
        return None

    return {
        "url": url,
        "title": title_tag.get_text(strip=True),
        "price": price_tag.get_text(strip=True).replace("Â","") if price_tag else None,
        "availability": availability_tag.get_text(strip=True) if availability_tag else None,
        "rating": rating_tag["class"][1] if rating_tag else None,
        "description": description_tag.get_text(strip=True) if description_tag else None,
    }

