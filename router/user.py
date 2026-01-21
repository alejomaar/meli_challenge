from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.deps import get_db
from model import User
from schema.api.user import CreateUserPayload, UserResponse

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create_user(
    payload: CreateUserPayload,
    db: AsyncSession = Depends(get_db),
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


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
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
