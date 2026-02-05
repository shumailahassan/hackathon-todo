from typing import AsyncGenerator, Callable, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.database.session import get_db_session

logger = logging.getLogger(__name__)


class TransactionManager:
    """
    A context manager for handling database transactions with automatic commit/rollback
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Exception occurred, rollback the transaction
            logger.error(f"Transaction failed with exception: {exc_val}")
            await self.session.rollback()
        else:
            # No exception, commit the transaction
            try:
                await self.session.commit()
            except SQLAlchemyError as e:
                logger.error(f"Commit failed: {e}")
                await self.session.rollback()
                raise


async def with_transaction(func: Callable[..., Any]) -> Any:
    """
    Decorator to wrap functions with automatic transaction management
    """
    async def wrapper(*args, **kwargs):
        async with get_db_session() as db_session:
            async with TransactionManager(db_session) as tx_session:
                # Replace the session in kwargs with the transaction session
                kwargs['db'] = tx_session
                result = await func(*args, **kwargs)
                return result
    return wrapper


# Alternative function-based approach
async def execute_in_transaction(operation: Callable[[AsyncSession], Any]) -> Any:
    """
    Execute a database operation within a transaction

    Args:
        operation: A function that takes an AsyncSession and performs database operations

    Returns:
        The result of the operation
    """
    async with get_db_session() as db_session:
        try:
            result = await operation(db_session)
            await db_session.commit()
            return result
        except Exception as e:
            await db_session.rollback()
            logger.error(f"Transaction failed: {str(e)}")
            raise


# Context manager for manual transaction control
def transaction_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for manual transaction control
    Usage:
        async with transaction_context() as tx_session:
            # Perform database operations
            await tx_session.commit()  # or rollback()
    """
    return get_db_session()