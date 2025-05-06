import logging
import random
import time

logger = logging.getLogger(__name__)


def retry_request(send_fn, max_retries=3, base_delay=0.5, jitter=0.1):
    """
    Retry a request function with exponential backoff and jitter.

    Args:
        send_fn (callable): Function that sends the request and returns a response.
        max_reties (int): Number of retries before giving up.
        base_delay (float): Base delay in seconds.
        jitter (float): Max jitter to add/subtract in seconds.

    Returns:
        Response object or None
    """

    for attempt in range(max_retries):
        try:
            response = send_fn()
            if response and response.status_code < 500:
                return response
        except Exception as e:
            logger.warning(f"Retry {attempt + 1} / {max_retries} failed: {e}")

        delay = base_delay * (2**attempt) + random.uniform(-jitter, jitter)
        time.sleep(max(delay, 0))

        logger.error("All retry attempts failed. ")
        return None
