from datetime import datetime

from pydantic import BaseModel, SecretStr, EmailStr, PositiveInt, field_validator
from pydantic_core import PydanticCustomError


class User(BaseModel):
    id: PositiveInt
    username: str
    password: SecretStr
    email: EmailStr
    created_at: datetime = datetime.now()

    @field_validator("username")
    def check_username_not_empty(cls, v: str):
        if ' ' in v:
            raise ValueError("Must not contain a space")
        return v

    @field_validator("password")
    def check_password_not_empty(cls, v: SecretStr):
        if ' ' in v.get_secret_value():
            raise ValueError("Must not contain a space")
        return v


    @field_validator("email")
    def check_valid_emails(cls, v: str):
        domains = ["gmail.com", "yahoo.com", "hotmail.com"]
        domain = v.split("@")[-1]
        if domain not in domains:
            raise PydanticCustomError(
                "Not a valid email address",
                'email address should contain at least one accepted domain names. Got "{domain}"',
                dict(domain=domain, acceptable_domains=domains)
            )
        return v

    class config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "passowrd": "*********",
                "email": "john.doe@mail.com",
                "created_at": "2020-12-05",
            }
        }
