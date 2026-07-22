from scraperflow.fetcher import fetch_page
from scraperflow.parser import parse_article
from scraperflow.storage import save_records
from scraperflow.cli import fetch_args
from scraperflow.config import SiteConfig
import logging


logger = logging.getLogger(__name__)

class Scraper:
    def orchestrate_scraper(self, config:SiteConfig):

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
                logger.warning(f"{config.domain} | Skipping URL: {url} as HTML response was not received")
                continue
            else:
                parsed_data = parse_article(html,url,config)
                if parsed_data is None:
                    logger.warning(f"{config.domain} | Data is not parsed for URL: {url}")
                else:
                    logger.info(f"{config.domain} | URL: {url} parsing is completed")
                    output_data.append(parsed_data)
            
        if output_data!=[]:
            save_records(output_data, output_path=args.output)
            logger.info(f"Data is saved in json")


