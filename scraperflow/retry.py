from scraperflow.exceptions import TransientFetchError
from functools import wraps
import time
import random
import logging

logger = logging.getLogger(__name__)


def calculate_delay(attempt: int, base_delay: float = 1.0, max_delay: float = 60.0) -> float:
    """Full jitter backoff: random between 0 and exponential ceiling."""
    ceiling = min(max_delay, base_delay * (2 ** attempt))
    return random.uniform(0, ceiling)

def retry(max_attempts=3, base_delay=1.0, max_delay=60.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except TransientFetchError as e:
                    if attempt == max_attempts - 1:
                        raise
                    delay = calculate_delay(attempt=attempt, base_delay=base_delay, max_delay=max_delay)
                    logger.warning(f"{func.__name__} failed (attempt {attempt + 1}/{max_attempts}): {e}. Retrying in {delay:.2f}s")
                    time.sleep(delay)
        return wrapper
    return decorator

