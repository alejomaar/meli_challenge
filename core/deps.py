from typing import AsyncGenerator

from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import settings
from model import (
    User,
)

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=5,
    pool_timeout=5,
    pool_recycle=30,
    pool_pre_ping=True,
    echo=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get AsyncSession.
    Ensures rollback on error and proper resource cleanup.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def get_current_user(
    x_user_id: int = Header(..., alias="X-User-Id"),
    db: AsyncSession = Depends(get_db),
) -> User:
    user = await db.scalar(select(User).where(User.id == x_user_id))

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User does not exist",
        )

    return user
