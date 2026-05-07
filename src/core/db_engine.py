"""Движок базы данных."""

import logging

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.core import conf

logger = logging.getLogger(__name__)
engine = create_async_engine(conf.postgres.dsn, echo=False)

session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

from src.db.models import User, WhitelistedPhrases, BlacklistedPhrases, Group  # noqa


@asynccontextmanager
async def get_session():
    """Генератор сессий."""
    async with session_factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database transaction error: {e}")
            raise
        finally:
            await session.close()
