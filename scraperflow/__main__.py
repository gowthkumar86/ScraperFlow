from scraperflow.scraper import Scraper
from scraperflow.config import SelectorMap, SiteConfig

# Bookstoscrape
bookstoscrape_selector_map = SelectorMap(title='.col-sm-6.product_main h1',
                                         price='.col-sm-6.product_main .price_color',
                                         description='.product_page>p', 
                                         product_image='.thumbnail img')
bookstoscrape_site_config = SiteConfig(domain='bookstoscrape.com',
                                       url='https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html',
                                       selectors=bookstoscrape_selector_map)

# #carwebsite
car_website_selector_map = SelectorMap(title='h2.title',
                                       description='p[itemprop="description"]',
                                       product_image='.main-image img')

car_website_site_config = SiteConfig(domain= 'webscraper.io/test-sites',
                                     url='https://webscraper.io/test-sites/product/mercedes-benz-w123-280e-1955-c001',
                                     selectors=car_website_selector_map)

# httpco.de — returns exact HTTP status codes, useful for testing retry/exception behavior
httpcode_selector_map = SelectorMap(title='h1')
httpcode_site_config = SiteConfig(domain='httpco.de',
                                   url='https://httpco.de',
                                   selectors=httpcode_selector_map)

scraper = Scraper()
# scraper.orchestrate_scraper(bookstoscrape_site_config)
# scraper.orchestrate_scraper(car_website_site_config)
scraper.orchestrate_scraper(httpcode_site_config)  # use with --urls https://httpco.de/200 https://httpco.de/404 https://httpco.de/503
