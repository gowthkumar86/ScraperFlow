import logging, sys
import argparse
from scraperflow.fetcher import fetch_page
from scraperflow.parser import parse_article
from scraperflow.storage import save_records

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


def orchestrate_scraper():

    output_data = []

    args = fetch_args()
    args = args.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.urls is None:
        logger.error("Enter url in the CLI command")
        return None
    
    urls = list(args.urls) if args.urls else []

    if args.url_file:
        with open(args.url_file, "r") as f:
            urls.extend(line.strip() for line in f if line.strip())

    if not urls:
        logger.error("No URLs provided via arguments or --url-file")
        return None
    
    for url in urls:
        try:
            html = fetch_page(url)
        except Exception as e:
            logger.warning(f"Skipping URL: {url} as HTML response was not received")
            continue
        else:
            parsed_data = parse_article(html,url)
            if parsed_data is None:
                logger.warning(f"Data is not parsed for URL: {url}")
            else:
                logger.info(f"URL: {url} parsing is completed")
                output_data.append(parsed_data)
        
    if output_data!=[]:
        save_records(output_data, output_path=args.output)
        logger.info(f"Data is saved in json")


