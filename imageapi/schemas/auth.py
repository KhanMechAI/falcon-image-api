from enum import Enum
from pydantic import BaseModel, Field, EmailStr, SecretStr


class RegisterSchema(BaseModel):
    email: str = EmailStr("api_user@imageapi.com.au")
    password: str = SecretStr("mystrongpassword")

