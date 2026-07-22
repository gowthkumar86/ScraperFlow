import logging, sys
import argparse


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("scraperflow/scraper.log", mode="a"),
    ]
)

logger = logging.getLogger(__name__)


def fetch_args() -> argparse.ArgumentParser:

    args = argparse.ArgumentParser(description="ScraperFlow V1 - fetching, parsing, storage")

    args.add_argument(
        "urls",
        nargs="*",
        default=[],
        help="URLs to scrape"
    )

    args.add_argument(
        "--output",
        default="output.json",
        help= "Output file_path"
    )

    args.add_argument(
        "--url-file",
        help="Path to a text file with one URL per line"
    )

    args.add_argument(
        "--verbose","--v",
        action="store_true"
    )
    
    return args
