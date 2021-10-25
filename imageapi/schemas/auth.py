from enum import Enum
from pydantic import BaseModel, Field, EmailStr, SecretStr


class RegisterSchema(BaseModel):
    email: str = EmailStr("api_user@imageapi.com.au")
    password: str = SecretStr("mystrongpassword")


class AlreadyRegisteredSchema(BaseModel):
    title: str = "User already exists",
    description: str = "User already registered"


class LoginSchema(RegisterSchema):
    email: str = EmailStr("api_user@imageapi.com.au")
    password: str = SecretStr("mystrongpassword")

