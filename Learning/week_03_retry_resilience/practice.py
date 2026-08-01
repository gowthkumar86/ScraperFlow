"""
Week 03: Retry & Resilience
ScraperFlow Version: V3
Concepts: decorators (function decorators, functools.wraps, decorator factories, closures),
          custom exception hierarchies, cross-cutting concerns, exponential backoff with jitter,
          transient vs. permanent failure classification, monkeypatching time.sleep
"""

import time
import functools
import requests

# --- Python Concepts: Closures ---

# Exercise 1: Basic closure
# Write a function `make_counter()` that returns an inner function.
# Each call to the inner function should return the next integer (0, 1, 2, ...).
# Do NOT use a class — use a closure with a mutable object (e.g., list) to hold state.
# Demonstrate that two separate counters maintain independent state.
def make_counter():
    x = [0]
    def inner():
        current = x[-1]
        x[-1] = x[-1]+1
        return current
    return inner

print("="*50)
print("Exercise-1")
print("="*50)
c1 = make_counter()
print(c1())
print(c1())
c2 = make_counter()
print(c2())
print(c2())

# Exercise 2: Closure capturing variables
# Write a function `make_multiplier(factor)` that returns a function which multiplies
# its argument by `factor`. Create multipliers for 3 and 7. Show that:
# - multiply_by_3(5) == 15
# - multiply_by_7(5) == 35
# Then explain: where does `factor` live after `make_multiplier` returns?
def make_multiplier(factor):
    def inner(y):
        return y*factor
    return inner

print("="*50)
print("Exercise-2")
print("="*50)

multiply_by_3 = make_multiplier(3)
print(f"multiply_by_3(5) {multiply_by_3(5)}")
multiply_by_7 = make_multiplier(7)
print(f"multiply_by_7(5) {multiply_by_7(5)}")

print(multiply_by_3.__closure__[0].cell_contents)
print("After `make_multiplier` returns, factor lives in a cell object attached to the inner function's __closure__ tuple")



# --- Python Concepts: Decorators ---

# Exercise 3: Basic decorator (no arguments)
# Write a decorator `log_call` that prints the function name and its arguments
# before calling it, and prints the return value after.
# Apply it to a function `add(a, b)` and call add(3, 4).
# Verify that the decorator is transparent (add(3, 4) still returns 7).
def log_call_without_wraps(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        items = list(args)
        print('Input values are '+','.join([str(item) for item in items]))
        result = func(*args, **kwargs)
        print('Output is', result)
        return result
    return wrapper

@log_call_without_wraps
def add(a,b):
    """Adds values that are passed as inputs"""
    return a+b

print("="*50)
print("Exercise-3")
add(3,4)



# Exercise 4: functools.wraps
# Take your `log_call` decorator from Exercise 3. WITHOUT functools.wraps, check:
#   print(add.__name__)   -> what does it print?
#   print(add.__doc__)    -> what does it print?
# Now add @functools.wraps(func) to the wrapper and check again.
# Explain why preserving metadata matters for debugging and introspection.
print("="*50)
print("Exercise-4")
print("From Exercise-3, add(3,4) is: "+add.__name__)
print(add.__doc__)

def log_call_with_wraps(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        items = list(args)
        print('Input values are '+','.join([str(item) for item in items]))
        result = func(*args, **kwargs)
        print('Output is', result)
        return result
    return wrapper

@log_call_with_wraps
def add(a,b):
    """Adds values that are passed as inputs"""
    return a+b

print("From Exercise-4, add(3,4) is: "+add.__name__)
print(add.__doc__)

# Exercise 5: Decorator factory (decorator with parameters)
# Write a decorator factory `repeat(n)` that calls the decorated function `n` times
# and returns a list of all return values.
# Usage:
#   @repeat(3)
#   def greet(name):
#       return f"Hello, {name}!"
#
#   greet("Alice")  # -> ["Hello, Alice!", "Hello, Alice!", "Hello, Alice!"]
#
# This requires THREE levels of nesting. Identify which level is:
#   1. The factory (receives decorator arguments)
#   2. The decorator (receives the function)
#   3. The wrapper (receives the function's arguments)

def repeat(n_times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result =[]
            for i in range(n_times):
                result.append(func(*args, **kwargs))
            print(result)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    return f"Hello, {name}!"

print("="*50)
print("Exercise-5")
greet("Hello Alice!")

# Exercise 6: Decorator that modifies control flow
# Write a decorator `suppress_exceptions(*exc_types)` that catches the specified
# exception types and returns None instead of raising.
# Any exception NOT in exc_types should propagate normally.
#
#   @suppress_exceptions(ValueError, TypeError)
#   def risky(x):
#       return int(x)
#
#   risky("abc")  # -> None (ValueError suppressed)
#   risky(None)   # -> None (TypeError suppressed)
#   risky("5")    # -> 5 (no exception)

def suppress_exceptions(*exec_types):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exec_types:
                return None
        return wrapper
    return decorator

@suppress_exceptions(ValueError, TypeError)
def risky(x):
    return int(x)

print("="*50)
print("Exercise-6")
print(risky('abc'))
print(risky(5))
print(risky(None))



# --- Python Concepts: Custom Exception Hierarchies ---

# Exercise 7: Exception hierarchy design
# Design an exception hierarchy for a file processing system:
#   - FileProcessingError (base)
#     - ReadError (file couldn't be read)
#       - FileNotFoundError_ (file doesn't exist — use trailing underscore to avoid shadowing builtin)
#       - PermissionError_ (no read permission)
#     - ParseError (file contents invalid)
#       - MalformedJSONError
#       - EncodingError
#     - WriteError (output couldn't be written)
#
# Implement all classes (they can be empty bodies with `pass`).
# Then write a try/except that catches at the ReadError level and demonstrate
# that it catches both FileNotFoundError_ and PermissionError_.

class FileProcessingError(Exception):
    pass

class ReadError(FileProcessingError):
    # def __init__(self, *args):
    #     super().__init__(*args)
    pass


class FileNotFoundError_(ReadError):
    def __init__(self, file_name, message):
        super().__init__(f"File Not Found Error, file_name:{file_name}, message:{message}")

class PermissionError_(ReadError):
    def __init__(self, file_name, message):
        super().__init__(f"Permission Error, file_name:{file_name}, message:{message}")

class ParseError(FileProcessingError):
    pass

class MalformedJSONError(ParseError):
    pass

class EncodingError(ParseError):
    pass

class WriteError(FileProcessingError):
    pass


def simulate_error(file_message):
    if file_message=='Could not find the file':
        raise FileNotFoundError_('file_1','File is not found')
    elif file_message=='No permission':
        raise PermissionError_('file_1','Permission denied')

print("="*50)
print("Exercise-7")

file_message = 'Could not find the file'
try:
    simulate_error(file_message)
except ReadError as exec:
    print(exec)


# Exercise 8: Exception with context
# Create a `RetryExhaustedError` exception class that stores:
#   - original_exception: the last exception that caused the final failure
#   - attempts: how many attempts were made
#   - total_delay: total seconds spent in backoff
# Override __str__ to produce a useful message like:
#   "Failed after 3 attempts (2.4s total delay): Connection timed out"

class RetryExhaustedError(Exception):

    def __init__(self,original_exception, attempts:int, total_delay:float):
        self.original_exception = original_exception
        self.attempts = attempts
        self.total_delay = total_delay
        super().__init__(f"Failed after {self.attempts} attempts ({self.total_delay}s total delay): {self.original_exception}")


print("="*50)
print("Exercise-8")
try:
    raise RetryExhaustedError(
        original_exception=ConnectionError("Connection timed out"),
        attempts=3,
        total_delay=2.4
    )
except RetryExhaustedError as e:
    print(e)  # "Failed after 3 attempts (2.4s total delay): Connection timed out"

# --- Architecture / Design Exercises ---

# Exercise 9: Cross-cutting concern identification
# Given this code, identify which parts are "business logic" and which are
# "cross-cutting concerns." Then refactor by extracting the cross-cutting
# concerns into decorators.
#
# def fetch_page(url):
#     start = time.time()
#     print(f"[INFO] Fetching {url}")
#     try:
#         for attempt in range(3):
#             try:
#                 response = requests.get(url, timeout=10)
#                 response.raise_for_status()
#                 duration = time.time() - start
#                 print(f"[INFO] Fetched {url} in {duration:.2f}s")
#                 return response.text
#             except requests.Timeout:
#                 delay = 2 ** attempt
#                 print(f"[WARN] Attempt {attempt+1} timed out, retrying in {delay}s")
#                 time.sleep(delay)
#     except Exception as e:
#         duration = time.time() - start
#         print(f"[ERROR] Failed to fetch {url} after {duration:.2f}s: {e}")
#         raise
#
# Which parts are: logging? timing? retry? actual fetching?
# Write the refactored version with each concern in its own decorator.

# Answer Part-1:
# Logging code : print(f"[INFO] Fetching {url}"), print(f"[WARN] Attempt {attempt+1} timed out, retrying in {delay}s") , print(f"[ERROR] Failed to fetch {url} after {duration:.2f}s: {e}")
# timing is happening at start of a function and end of fetching the page, if error => after doing retry
# retry : we are doing a for loop
# fetching = requests.get(url, timeout=10)

def logging_fetch(func):
    @functools.wraps(func)
    def wrapper(url):
        print(f"[INFO] Fetching {url}")
        try:
            return func(url)
        except Exception as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")
            raise
    return wrapper

def timing_fetch(func):
    @functools.wraps(func)
    def wrapper(url):
        start = time.time()
        try:
            result = func(url)
            return result
        finally:
            duration = time.time() - start
            print(f"[TIMING] {func.__name__} took {duration:.2f}s")
    return wrapper

def retry_fetch(max_attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(url):
            for attempt in range(max_attempts):
                try:
                    return func(url)
                except requests.Timeout:
                    delay = 2 ** attempt
                    time.sleep(delay)
            raise Exception(f"Failed to fetch {url} after {max_attempts} attempts")
        return wrapper
    return decorator

@logging_fetch
@timing_fetch
@retry_fetch(max_attempts=3)
def fetch_page(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

print("="*50)
print("Exercise-9")
fetch_page("https://books.toscrape.com/")

# Exercise 10: Exponential backoff with jitter
# Implement a function `calculate_delay(attempt, base_delay=1.0, max_delay=60.0)`
# that returns the backoff delay for a given attempt number using FULL JITTER:
#   delay = random.uniform(0, min(max_delay, base_delay * 2 ** attempt))
#
# Generate 10 delays for attempts 0-9 and print them.
# Then generate 10 delays for attempt 5 repeated 10 times — show that jitter
# produces different values each time (not deterministic).
import random

def calculate_delay(attempt: int, base_delay: float = 1.0, max_delay: float = 60.0) -> float:
    """Full jitter backoff: random between 0 and exponential ceiling."""
    ceiling = min(max_delay, base_delay * (2 ** attempt))
    return random.uniform(0, ceiling).__round__(2)

print("="*50)
print("Exercise-10")
# Generate 10 delays for attempts 0-9 and print them.
for i in range(0,10):
    print(f"Attempt-{i}: {calculate_delay(i)}")

# Then generate 10 delays for attempt 5 repeated 10 times — show that jitter
# for n in range(0,10):
print("Attempt 5 repeated 10 times "+str([f"{calculate_delay(5)}" for _ in range(0,10)]))

# Exercise 11: Transient vs. permanent classification
# Given a list of HTTP status codes, classify each as transient (worth retrying)
# or permanent (don't bother). Write a function `classify_http_error(status_code)`
# that returns "transient" or "permanent".
#
# Test with: 200, 400, 401, 403, 404, 408, 429, 500, 502, 503, 504
# Explain your reasoning for each classification. Which ones are debatable?

TRANSIENT_CODES = {408, 429, 500, 502, 503, 504}

def classify_http_error(status_code: int) -> str:
    if status_code in TRANSIENT_CODES:
        return "transient"
    return "permanent"

print("="*50)
print("Exercise-11")
test_codes = [200, 400, 401, 403, 404, 408, 429, 500, 502, 503, 504]
for code in test_codes:
    print(f"  {code}: {classify_http_error(code)}")

# Reasoning:
# 408 Request Timeout — server-side timeout, may resolve on retry
# 429 Too Many Requests — rate limited, back off and retry
# 500 Internal Server Error — often transient overload
# 502 Bad Gateway — upstream issue, usually temporary
# 503 Service Unavailable — explicitly temporary
# 504 Gateway Timeout — upstream slow, may resolve
# 400, 401, 403, 404 — our request is wrong or resource doesn't exist, won't fix itself
# Debatable: 403 (some sites use it for rate limiting), 500 (could be a persistent bug)


# --- Testing Concepts ---

# Exercise 12: Monkeypatching time.sleep
# Write a retry decorator (simplified: fixed delay, 3 attempts, retries on ValueError).
# Then write a test that:
#   1. Monkeypatches time.sleep to record delays instead of actually sleeping
#   2. Verifies the decorator retried the correct number of times
#   3. Verifies the sleep durations match expectations
#   4. Runs in milliseconds, not seconds
#
# Use either pytest's monkeypatch fixture pattern or unittest.mock.patch.

from unittest.mock import patch

def simple_retry(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        last_exception = None
        for attempt in range(3):
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                last_exception = e
                time.sleep(1.0)
        raise last_exception
    return wrapper

def test_retry_monkeypatch():
    sleep_calls = []

    # Stub that fails twice then succeeds
    call_count = [0]
    @simple_retry
    def flaky():
        call_count[0] += 1
        if call_count[0] <= 2:
            raise ValueError(f"fail #{call_count[0]}")
        return "success"

    with patch("time.sleep", side_effect=lambda s: sleep_calls.append(s)):
        result = flaky()

    assert result == "success", f"Expected 'success', got {result}"
    assert call_count[0] == 3, f"Expected 3 calls, got {call_count[0]}"
    assert len(sleep_calls) == 2, f"Expected 2 sleeps, got {len(sleep_calls)}"
    assert all(d == 1.0 for d in sleep_calls), f"Expected all delays=1.0, got {sleep_calls}"
    print("test_retry_monkeypatch PASSED")

print("="*50)
print("Exercise-12")
test_retry_monkeypatch()


# --- Challenge ---

# Challenge: Production-grade retry decorator
# Build a complete retry decorator factory that:
# 1. Accepts: max_attempts (int), base_delay (float), max_delay (float)
# 2. Retries ONLY on a specified exception type (passed as parameter)
# 3. Uses exponential backoff with full jitter
# 4. Logs each retry attempt (attempt number, delay, exception message)
# 5. Preserves the wrapped function's metadata (functools.wraps)
# 6. Re-raises the last exception if all attempts are exhausted
# 7. Is completely transparent when the function succeeds on the first attempt
#
# Then write a test (without pytest — just assertions) that:
# - Monkeypatches time.sleep to a no-op
# - Verifies retry count
# - Verifies the decorator doesn't catch exceptions it shouldn't
#
# This is essentially what you'll build for ScraperFlow V3.
