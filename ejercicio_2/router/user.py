from core.deps import get_db
from fastapi import APIRouter, Depends, status
from schema.api.user import CreateUserPayload, UserResponse
from service.user import use_case_create_user, use_case_get_user
from sqlalchemy.ext.asyncio import AsyncSession

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

    return await use_case_create_user(payload, db)


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

    return await use_case_get_user(user_id, db)
