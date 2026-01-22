from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from gtree.core.config.settings import settings


def create_engine(url: str, is_echo: bool = True) -> AsyncEngine:
    """Creates an asynchronous SQLAlchemy engine.

    Args:
        url: The database connection URL.
        is_echo: If True, SQL statements will be echoed to the console.

    Returns:
        An AsyncEngine instance.
    """
    return create_async_engine(
        url=url,
        echo=is_echo,
        pool_size=20,
        max_overflow=30,
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={},
    )


def get_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Creates an asynchronous sessionmaker for SQLAlchemy sessions.

    Args:
        engine: The AsyncEngine instance.

    Returns:
        An async_sessionmaker configured for AsyncSession.
    """
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


engine = create_engine(settings.database.sqlalchemy_database_uri)
session_factory = get_session_factory(engine)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
