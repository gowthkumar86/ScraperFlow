
class ScraperFlowError(Exception):
    """Base exception for all ScraperFlow errors."""

class FetchError(ScraperFlowError):
    """Base for all Fetcher Errors"""
    def __init__(self, *args):
        super().__init__(*args)

class TransientFetchError(FetchError):
    """Failure that may resolve on retry (timeout, 5xx, rate limit)."""

class PermanentFetchError(FetchError):
    """Failure that will NOT resolve on retry (404, 410, bad URL)."""