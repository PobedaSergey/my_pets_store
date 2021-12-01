from pydantic import Field, validator
from pydantic import BaseModel as PydanticBaseModel
from typing import List
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError, EMAIL_MAX_LENGTH
from fastapi import HTTPException

from logs import *


class BaseModel(PydanticBaseModel):
    class Config:
        anystr_strip_whitespace = True


class PetBase(BaseModel):
    animal_name: str = Field(..., title="Кличка питомца")
    description: str = Field(None, title="Характерные черты питомца")

    class Config:
        schema_extra = {
            "example": {
                "animal_name": "Лапчик",
                "description": "Большая рыжая собака"
            }
        }


class PetCreate(PetBase):
    pass


class Pet(PetBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str = Field(...,
                       title="Введите email",
                       example="example@mail.ru")

    @validator('email')
    def check_email(cls, email):
        if len(email) >= EMAIL_MAX_LENGTH:
            logger.info(f'Введен слишком длинный email: "{email}", создание пользователя провалено')
            raise HTTPException(status_code=422, detail="Введен слишком длинный email")
        try:
            valid = validate_email(email, check_deliverability=True)
            email = valid.email
            return email
        except (EmailNotValidError, EmailSyntaxError) as e:
            logger.info(f'Введен некорректный email: "{email}", создание пользователя провалено')
            raise HTTPException(status_code=422, detail=str(e))


class UserCreate(UserBase):
    password: str = Field(...,
                          title="Введите пароль, минимум 8 символов",
                          example="example_password", min_length=8)


class User(UserBase):
    id: int
    pets: List[Pet] = []

    class Config:
        orm_mode = True
