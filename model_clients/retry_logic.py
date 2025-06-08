import functools
import random
import time
from handlers.logger import logger


def retry_with_exponential_backoff(
        max_retries: int=5,
        initial_delay: int=2,
        max_delay: int=70,
        backoff_factor: int=2,
        jitter: float=0.1
):
    """
    Retry decorator with exponential backoff for API rate limits

    Args:
        max_retries: Maximum number of retries
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        backoff_factor: Factor to increase delay with each retry
        jitter: Random jitter factor to add to delay
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay

            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error_str = str(e)
                    # Check if it's a rate limit error (429)
                    if retries >= max_retries or "429" not in error_str:
                        # If we've exhausted retries or it's not a rate limit error
                        raise

                    # Extract wait time if available in the error message
                    wait_time = 60  # Default to 60 seconds
                    import re
                    time_match = re.search(r'retry after (\d+) seconds', error_str.lower())
                    if time_match:
                        wait_time = int(time_match.group(1))

                    # Add some randomness to the delay
                    jitter_amount = delay * jitter * random.uniform(-1, 1)
                    sleep_time = min(max(wait_time, delay + jitter_amount), max_delay)

                    # Log the retry
                    logger.warning(
                        f"Rate limit exceeded (429). Retrying in {sleep_time:.2f} seconds. "
                        f"Retry {retries + 1}/{max_retries}"
                    )

                    # Sleep and retry
                    time.sleep(sleep_time)
                    retries += 1
                    delay = min(delay * backoff_factor, max_delay)

        return wrapper

    return decorator
