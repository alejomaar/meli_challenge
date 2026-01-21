# schema/api/user.py
from pydantic import BaseModel


class CreateUserPayload(BaseModel):
    nickname: str


class UserResponse(BaseModel):
    id: int
    nickname: str
