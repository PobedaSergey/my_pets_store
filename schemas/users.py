from typing import List
from fastapi import HTTPException
from pydantic import Field, validator
from email_validator import validate_email, EmailNotValidError, EmailSyntaxError, EMAIL_MAX_LENGTH

from repositories.logs import logger
from schemas.base_schemas import ModBaseModel
from schemas.pets import PetSchemas


class UserBase(ModBaseModel):
    email: str = Field(
        ...,
        title="Введите email",
        example="example@mail.ru"
    )

    @classmethod
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
    password: str = Field(
        ...,
        title="Введите пароль, минимум 8 символов",
        example="example_password", min_length=8
    )


class UserSchemas(UserBase):
    id: int
    pets: List[PetSchemas] = []

    class Config:
        orm_mode = True
