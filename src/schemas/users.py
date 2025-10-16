from datetime import date

from pydantic import BaseModel, Field, EmailStr, constr

from src.models.users import RoleEnum


class UserRequestAddRegister(BaseModel):
    first_name: str | None = Field("John")
    last_name: str | None = Field("Doe")
    nickname: str = constr(strip_whitespace=True, min_length=1), Field(...)
    birth_day: date | None = None
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserAdd(BaseModel):
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    nickname: str = Field(..., min_length=1)
    birth_day: date | None = None
    email: EmailStr
    hashed_password: str
    role: RoleEnum = Field(default=RoleEnum.user)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_day: date
    nickname: str
    email: EmailStr
    role: RoleEnum = Field(default=RoleEnum.user)


class UserWithHashedPassword(User):
    hashed_password: str