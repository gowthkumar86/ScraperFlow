"""
Week 02: Config-Driven Multi-Site
ScraperFlow Version: V2
Concepts: @dataclass (fields, defaults, frozen, __post_init__), composition over inheritance,
          configuration as data vs. code, essential vs. coincidental duplication (Rule of Three),
          DevTools site inspection, designing SiteConfig
"""

from dataclasses import FrozenInstanceError, dataclass, field, fields


# --- Python Concepts: @dataclass ---

# Exercise 1: Basic dataclass
# Create a dataclass called `Book` with fields: title (str), price (float), in_stock (bool).
# Instantiate two Book objects and print them.
# Observe the auto-generated __repr__, __eq__, and __init__.

@dataclass
class Book:
    title : str
    price : float
    in_stock : bool

print("="*50+"Exercise 1","="*50)
book1 = Book('Harry Potter', 22.5, True)
book2 = Book('Psychology of Money',price = 15.99,in_stock= False)
print (book1)
print (book2)
print(book1 == Book('Harry Potter', 22.5, True))


# Exercise 2: Defaults and field ordering
# Create a dataclass called `ScrapeResult` with:
# - url: str (no default)
# - title: str (no default)
# - timestamp: str (default to "unknown")
# - success: bool (default True)
# Instantiate one with all fields and one using only required fields.
@dataclass
class ScrapeResult:
    url : str
    title : str
    timestamp : str = "unknown"
    success : bool = True

print("="*50+"Exercise 2","="*50)
scrape1 = ScrapeResult(url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html", title= "A Light in the Attic", timestamp="1784703633", success=True)
scrape2 = ScrapeResult(url = "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html", title= "Tipping the Velvet")
print(scrape1)
print(scrape2)

# Exercise 3: frozen=True
# Create a frozen dataclass called `Credentials` with fields: username (str), token (str).
# Instantiate it, then try to modify the `token` field.
# Catch the FrozenInstanceError and print a message explaining why immutability matters here.
@dataclass(frozen=True)
class Credentials:
    username : str
    token : str

print("="*50+"Exercise 3","="*50)
user_1 = Credentials(username="David", token="dsf398yf3uhf9uh3f3j")
print(user_1)
try:
    user_1.token = 'csknef03jv03ij43v'  # type: ignore[misc]
except FrozenInstanceError:
    print("Credentials are frozen, so tokens cannot be changed after creation.")



# Exercise 4: __post_init__ validation
# Create a dataclass called `URLConfig` with fields: name (str), base_url (str).
# Add a __post_init__ method that raises ValueError if base_url doesn't start with "http".
# Test with both a valid and invalid URL.
@dataclass
class URLConfig:
    name : str
    base_url : str

    def __post_init__(self):
        if not self.base_url.startswith('http'):
            raise ValueError(f"Error in {self.base_url} .Base url should start with http")

print("="*50+"Exercise 4","="*50)
url1 = URLConfig(name="book1",base_url="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
print(url1)
try:
    url2 = URLConfig(name="book1",base_url="ht://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
    print(url2)
except ValueError as exc:
    print(exc)



# Exercise 5: field() with default_factory
# Create a dataclass called `PageData` with:
# - url: str
# - headers: dict (default to empty dict — use field(default_factory=dict))
# - tags: list[str] (default to empty list — use field(default_factory=list))
# Create two instances WITHOUT passing headers/tags. Mutate one's headers dict.
# Verify the other instance's headers dict is NOT affected (explain why default_factory matters).
@dataclass(frozen=True)
class PageData:
    url : str
    headers : dict[str,str] = field(default_factory=dict)
    tags : list[str] = field(default_factory=list)

print("="*50+"Exercise 5","="*50)
page_data_1 = PageData(url="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
print(page_data_1)
page_data_2 = PageData(url="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
print(page_data_2)
headers =  {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html",
    "Accept-Language": "en-US"
}
for i in headers:
    page_data_2.headers[i] = (headers.get(i))
    
print("After adding headers")
print(page_data_2)
print(page_data_1.headers)

# Exercise 6: Dataclass with methods
# Create a dataclass called `SelectorMap` with:
# - title: str
# - price: str
# - availability: str | None (default None)
# Add a method `required_fields()` that returns a list of field names where the value is not None.
# Add a method `as_dict()` that returns a dict of {field_name: selector} for non-None fields.

@dataclass
class SelectorMap:
    title : str
    price : str
    availability : str = None

    def required_fields(self):
        field_names = []
        for field in fields(self):
            if getattr(self,field.name) is not None:
                field_names.append(field.name)
        return field_names

    def as_dict(self):
        selector_dict = {}
        for field_name in self.required_fields():
            selector_dict[field_name] = getattr(self,field_name)
        return selector_dict
            
selector_config1 = SelectorMap(
    title="h1",
    price="p.price_color",
    availability="p.instock"
)

selector_config2 = SelectorMap(
    title="h1.product_main h1",
    price="p.price_color"
)

print("="*50+"Exercise 6","="*50)
print(f"With availablility : {selector_config1}")
print(f"Required fields: {selector_config1.required_fields()}")
print(f"Required fields: {selector_config1.as_dict()}")
print(f"Without availablility : {selector_config2}")


    


# --- Architecture / Design Exercises ---

# Exercise 7: Composition over inheritance
# You have two sites to scrape. Write TWO approaches:
#
# Approach A (inheritance — the wrong fit here):
#   - BaseScraper with a scrape() method
#   - BooksScraper(BaseScraper) with hardcoded selectors
#   - NewsScraper(BaseScraper) with hardcoded selectors        
#
# Approach B (composition — the right fit):
#   - A SiteConfig dataclass holding selectors
#   - A single Scraper class/function that accepts SiteConfig
#   - Two SiteConfig instances (one per site)
#
# Implement BOTH skeleton approaches (no real scraping — just print what would happen).
# Then write a comment explaining:
#   - Which approach requires less code to add a third site?
#   - Which approach has tighter coupling between the scraper logic and site-specific details?
#   - Under what circumstances would inheritance actually be the better choice?

class BaseScraper:
    def scrape(self, url: str) -> None:
        print(f"Fetching {url}")
        print("Parsing with scraper-specific logic")


class BooksScraper(BaseScraper):
    def scrape(self, url: str) -> None:
        print(f"Fetching books site: {url}")
        print("Using hardcoded book selectors")


class NewsScraper(BaseScraper):
    def scrape(self, url: str) -> None:
        print(f"Fetching news site: {url}")
        print("Using hardcoded news selectors")

@dataclass
class SiteConfig:
    name: str
    base_url: str
    selectors: dict[str, str]
    description: str = ""
    
class Scraper:
    def scrape_site(self, config: SiteConfig) -> dict[str, str]:
        print(f"Fetching {config.name}: {config.base_url}")
        print(f"Using selectors from config: {config.selectors}")
        return {field_name: f"matched {selector}" for field_name, selector in config.selectors.items()}


print("=" * 50 + "Exercise 7", "=" * 50)
print("Inheritance approach:")
BooksScraper().scrape("https://books.toscrape.com")
NewsScraper().scrape("https://news.example.com")

print("Composition approach:")
books_config = SiteConfig(
    name="books",
    base_url="https://books.toscrape.com",
    selectors={"title": ".product_main h1", "price": ".price_color"},
    description="Book catalog site",
)
news_config = SiteConfig(
    name="news",
    base_url="https://news.example.com",
    selectors={"title": "h1", "date": ".date"},
    description="News site",
)

scraper = Scraper()
print(scraper.scrape_site(books_config))
print(scraper.scrape_site(news_config))

# To add a third site, the composition approach needs only one new SiteConfig instance.
# The inheritance approach needs a new subclass with its own hardcoded selectors.
# Inheritance is the better choice only when the variation is behavior, not just data,
# or when subclasses need to override several steps of the algorithm.

# Exercise 8: Essential vs. coincidental duplication
# Below are two functions. Determine if the duplication is essential or coincidental.
# Write a comment with your reasoning and whether you would refactor.
#
# def parse_books_page(html):
#     soup = BeautifulSoup(html, "html.parser")
#     title = soup.select_one("h1").text
#     price = soup.select_one(".price").text
#     return {"title": title, "price": price}
#
# def parse_news_page(html):
#     soup = BeautifulSoup(html, "html.parser")
#     title = soup.select_one("h1").text
#     date = soup.select_one(".date").text
#     return {"title": title, "date": date}

# Answer:
# This duplication is mostly coincidental, not essential.
# Both functions share the same parsing setup and the same extraction pattern,
# but the actual fields being selected are different per page type.
# I would refactor the shared parsing setup into a helper, then keep the page-specific
# selectors separate so the code stays config-driven and easy to extend.



# Exercise 9: Configuration as data
# Given this hardcoded function:
#
# def scrape_books():
#     url = "https://books.toscrape.com"
#     title_selector = ".product_main h1"
#     price_selector = ".price_color"
#     # ... fetch, parse, store
#
# Refactor it so that url and selectors come from a dataclass instance
# passed as a parameter. The function body should contain zero site-specific strings.

@dataclass
class SiteConfiguration:
    url : str
    title : str
    price : str

def scrape_books(config:SiteConfiguration):
    url = config.url
    title_selector = config.title
    price_selector = config.price
    return {
        "title": title_selector,
        "url" : url,
        "price": price_selector
    }

books_config = SiteConfiguration(
    url="https://books.toscrape.com",
    title=".product-name",
    price = ".product-price"
)

print("=" * 50 + "Exercise 9", "=" * 50)
output = scrape_books(books_config)
print(output)



# --- Challenge ---

# Challenge: Multi-site config system
# Design and implement a complete (but minimal) config-driven scraping system:
# 1. A SiteConfig dataclass with: name, base_url, selectors (dict[str, str]), and an optional
#    description field with a default.
# 2. A function `scrape_site(config: SiteConfig, html: str) -> dict` that uses the config's
#    selectors to extract data from HTML. The function must not reference any specific
#    site by name — it works purely from the config's data.
# 3. Two SiteConfig instances for two different (real or fictional) sites.
# 4. Demonstrate that both configs work through the same function.
# 5. Write a comment explaining: if you needed to add a third site, what would you change?
#    (Answer should be: "only add a new SiteConfig instance.")
