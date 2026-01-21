from fastapi import HTTPException
from model import User
from schema.api.user import CreateUserPayload, UserResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def use_case_create_user(
    payload: CreateUserPayload,
    db: AsyncSession,
):
    """
    Create a new user.

    Users are identified by a unique nickname and do not require
    passwords or authentication credentials.
    """

    user = User(nickname=payload.nickname)
    db.add(user)

    try:
        await db.flush()
        await db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="User with this nickname already exists",
        )

    return UserResponse(id=user.id, nickname=user.nickname)


async def use_case_get_user(
    user_id: int,
    db: AsyncSession,
):
    """
    Retrieve a user by identifier.
    """

    user = await db.scalar(
        select(User).where(User.id == user_id)
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return UserResponse(id=user.id, nickname=user.nickname)
