from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserSchema(BaseModel):
    id: int
    full_name: str = Field(max_length=128)
    username: str | None = Field(max_length=128)
    email: EmailStr = Field(max_length=128)
    phone: PhoneNumber | None
    # через конфиг дикт мы можем прям запретить другие поля передавать, у нас же мы можем провалидировать только нужные
    # а остальные так оставить


""" class UserLanguageSchema(BaseModel):
    language: str = Field(gt=1, lt=3)
    пайдантик позволяет наследовать схемы и если нам нужны разные валидации то мы можем сделать так
 """
