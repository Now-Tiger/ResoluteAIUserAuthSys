from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core import PydanticCustomError


class PasswordUpdater(BaseModel):
    old_password: str 
    new_password: str

    @field_validator("old_password")
    def valid_old_password(cls, v: str):
        if " " in v or "" == v:
            raise ValueError("Must not contain space nor it should be empty")
        return v

    @field_validator("new_password")
    def valid_new_password(cls, v: str):
        if " " in v or "" == v:
            raise ValueError("Must not contain space nor it should be empty")
        return v


class UserResponse(BaseModel):
    id: str
    email: EmailStr


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    email: EmailStr
    created_at: str = str(datetime.now(timezone.utc))

    @field_validator("username")
    def check_username_not_empty(cls, v: str):
        if ' ' in v:
            raise ValueError("Must not contain a space")
        elif '' == v:
            raise ValueError("Must not be empty")
        return v

    @field_validator("password")
    def check_password_not_empty(cls, v: str):
        if ' ' in v:
            raise ValueError("Must not contain a space")
        elif '' == v:
            raise ValueError("Must not be empty")
        return v


    @field_validator("first_name")
    def check_first_name_not_empty(cls, v: str):
        if ' ' in v or '' == v:
            raise ValueError("Must not empty nor have space")
        return v

    @field_validator("last_name")
    def check_last_name_not_empty(cls, v: str):
        if ' ' in v or '' == v:
            raise ValueError("Must not empty nor have space")
        return v

    @field_validator("email")
    def check_valid_emails(cls, v: str):
        acceptable_domains = ValidDomainsForMail().domains
        domain = v.split("@")[-1]
        if domain not in acceptable_domains:
            raise PydanticCustomError(
                "Not a valid email address",
                'email address should contain at least one accepted domain names. Got "{domain}"',
                dict(domain=domain, acceptable_domains=acceptable_domains)
            )
        return v


    class config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "*********",
                "email": "john.doe@mail.com",
            }
        }


class ValidDomainsForMail(BaseModel):
    domains: List[str] = ["gmail.com", "hotmail.com", "yahoo.com"]
