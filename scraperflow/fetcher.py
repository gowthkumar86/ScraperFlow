import requests
import logging
from scraperflow.exceptions import TransientFetchError, PermanentFetchError
from scraperflow.retry import retry

logger = logging.getLogger(__name__)

TRANSIENT_CODES = {408, 429, 500, 502, 503, 504}

@retry(max_attempts=3)
def fetch_page(url: str) -> str:
    logger.info(f"Fetching {url}")
    try:
        response = requests.get(url, timeout=10)
    except requests.ConnectionError as e:
        logger.error(f"Connection failed: {url}")
        raise TransientFetchError(f"Connection failed: {url}") from e
    except requests.Timeout as e:
        logger.error(f"Timeout: {url}")
        raise TransientFetchError(f"Timeout: {url}") from e

    if response.status_code == 200:
        logger.info(f"Fetched {url} successfully")
        return response.text
    elif response.status_code in TRANSIENT_CODES:
        logger.warning(f"HTTP {response.status_code}: {url}")
        raise TransientFetchError(f"HTTP {response.status_code}: {url}")
    else:
        logger.error(f"HTTP {response.status_code}: {url}")
        raise PermanentFetchError(f"HTTP {response.status_code}: {url}")