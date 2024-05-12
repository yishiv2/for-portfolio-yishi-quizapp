from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    username: str = Field(min_length=2, examples=["メールアドレス"])
    displayname: str = Field(min_length=5, examples=["ユーザー名"])
    password: str = Field(min_length=8, examples=["test1234"])


class UserResponse(BaseModel):
    displayname: str = Field(min_length=5, examples=["ユーザー名"])
    username: str = Field(min_length=2, examples=["user1"])


class Token(BaseModel):
    access_token: str
    token_type: str


class DecodedToken(BaseModel):
    username: str
    displayname: str
