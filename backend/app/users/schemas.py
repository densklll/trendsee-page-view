from datetime import datetime

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class UserUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class UserResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class UserCreateResponse(BaseModel):
    user: UserResponse
    token: str


class TokenResponse(BaseModel):
    token: str
