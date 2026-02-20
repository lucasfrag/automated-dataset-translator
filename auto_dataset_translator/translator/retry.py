import time
import random


class RetryConfig:

    def __init__(
        self,
        max_retries=5,
        base_delay=1.0,
        max_delay=30.0,
        jitter=True,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter


def retry_with_backoff(func, config: RetryConfig):

    last_exception = None

    for attempt in range(config.max_retries):

        try:
            return func()

        except Exception as e:

            last_exception = e

            delay = min(
                config.base_delay * (2 ** attempt),
                config.max_delay,
            )

            if config.jitter:
                delay *= random.uniform(0.5, 1.5)

            print(
                f"Retry {attempt+1}/{config.max_retries} "
                f"in {delay:.2f}s due to: {e}"
            )

            time.sleep(delay)

    raise last_exception