from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise ValueError("passwords don't match")
        return v


class UserLogin(BaseModel):
    prefix: Optional[str]
    email: Optional[EmailStr]
    password: str


class User(BaseModel):
    id: int
    name: str
    ava: Optional[str]
    prefix: Optional[str]


class UserWithToken(User):
    token: Token


class UserToUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    ava: Optional[str] = None
    prefix: Optional[str] = None
