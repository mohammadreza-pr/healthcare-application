from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Column, String
from enum import Enum
from typing import Optional, List


class Gender(Enum):
    MALE = "male",
    FEMALE = "female"


# Shared properties
class UserBase(SQLModel):
    phone_number: str = Field(unique=True, index=True, max_length=11)
    full_name: str | None = Field(default=None, max_length=255)
    national_id: str = Field(unique=True)


class UserRegister(UserBase):
    password: str = Field(min_length=8, max_length=40)
    gender: str
    birth_date: str
    height: int
    weight: int
    sickness: str
    sickness_history: Optional[List[str]] = Field(sa_column=Column(ARRAY(String)))
    family_sickness_history: Optional[List[str]] = Field(sa_column=Column(ARRAY(String)))
    medicines: Optional[List[str]] = Field(sa_column=Column(ARRAY(String)))
    allergies: Optional[List[str]] = Field(sa_column=Column(ARRAY(String)))


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserRegister, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str = Field(min_length=1, max_length=255)


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
