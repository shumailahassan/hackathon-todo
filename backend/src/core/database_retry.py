import asyncio
import logging
import random
from functools import wraps
from typing import Callable, TypeVar, Awaitable, Optional
from sqlalchemy.exc import SQLAlchemyError, DisconnectionError, OperationalError

logger = logging.getLogger(__name__)

T = TypeVar('T')

def retry_database_operation(
    max_retries: int = 3,
    base_delay: float = 0.1,
    max_delay: float = 5.0,
    exponential_base: float = 2.0,
    jitter: bool = True
):
    """
    Decorator to add retry logic for database operations

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries (seconds)
        max_delay: Maximum delay between retries (seconds)
        exponential_base: Base for exponential backoff calculation
        jitter: Whether to add random jitter to delay times
    """
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except (DisconnectionError, OperationalError, SQLAlchemyError) as e:
                    last_exception = e

                    # Check if this is a transient error worth retrying
                    error_msg = str(e).lower()
                    if not should_retry_error(error_msg):
                        logger.error(f"Non-transient error in {func.__name__}: {e}")
                        raise e

                    if attempt == max_retries:
                        logger.error(f"Max retries exceeded for {func.__name__} after {max_retries} attempts. Last error: {e}")
                        raise e

                    delay = calculate_delay(
                        attempt, base_delay, max_delay, exponential_base, jitter
                    )

                    logger.warning(
                        f"Attempt {attempt + 1} failed in {func.__name__}: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )

                    await asyncio.sleep(delay)

            # This shouldn't be reached, but included for type safety
            raise last_exception

        return wrapper
    return decorator


def should_retry_error(error_message: str) -> bool:
    """
    Determine if a database error should trigger a retry

    Args:
        error_message: The error message to check

    Returns:
        True if the error is likely transient and worth retrying
    """
    transient_indicators = [
        'connection', 'disconnection', 'timeout', 'deadlock',
        'concurrent', 'race', 'busy', 'try again', 'retry',
        'server has gone away', 'lost connection', 'network',
        'pool', 'exceeded', 'temporary'
    ]

    return any(indicator in error_message for indicator in transient_indicators)


def calculate_delay(
    attempt: int,
    base_delay: float,
    max_delay: float,
    exponential_base: float,
    jitter: bool
) -> float:
    """
    Calculate delay with exponential backoff and optional jitter

    Args:
        attempt: Current attempt number (0-indexed)
        base_delay: Base delay value
        max_delay: Maximum allowed delay
        exponential_base: Base for exponential calculation
        jitter: Whether to add random jitter

    Returns:
        Calculated delay in seconds
    """
    # Exponential backoff: base_delay * (exponential_base ^ attempt)
    delay = min(base_delay * (exponential_base ** attempt), max_delay)

    # Add jitter to prevent thundering herd problems
    if jitter:
        jitter_range = min(delay * 0.1, 1.0)  # Up to 10% or 1 second jitter
        delay += random.uniform(-jitter_range, jitter_range)
        delay = max(0, delay)  # Ensure non-negative

    return delay


# Example usage function for testing
async def example_database_call(db_session, query_func):
    """
    Example of how to use the retry decorator with database operations
    """
    @retry_database_operation(max_retries=3, base_delay=0.1)
    async def execute_query():
        return await query_func(db_session)

    return await execute_query()


# Context manager alternative for retry logic
class DatabaseRetryContext:
    """
    Context manager for retrying database operations
    """
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 0.1,
        max_delay: float = 5.0
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    async def execute(self, operation: Callable[[], Awaitable[T]]) -> T:
        """
        Execute an operation with retry logic
        """
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                return await operation()
            except (DisconnectionError, OperationalError, SQLAlchemyError) as e:
                last_exception = e

                if not should_retry_error(str(e).lower()):
                    logger.error(f"Non-transient error: {e}")
                    raise e

                if attempt == self.max_retries:
                    logger.error(f"Max retries exceeded after {self.max_retries} attempts. Last error: {e}")
                    raise e

                delay = calculate_delay(attempt, self.base_delay, self.max_delay, 2.0, True)

                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s...")
                await asyncio.sleep(delay)

        raise last_exception