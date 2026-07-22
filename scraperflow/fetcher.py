import requests
import logging, sys

logger = logging.getLogger(__name__)

def fetch_page(url:str) -> str:
    logger.info(f"Attempting to fetch URL {url}")
    response = requests.get(url)

    try:
        if response.status_code == 200:
            logger.info(f"URL: {url} fetched succesfully. status code: {response.status_code}")
            return response.text
    except:
        logger.error(f"Failed to fetch URL: {url}. Status Code: {response.status_code}")
        response.raise_for_status()
        return None