from pydantic import BaseModel, Field
from typing import List


class PetBase(BaseModel):
    title: str = Field(..., title="Кличка питомца")
    description: str = Field(None, title="Характерные черты питомца")

    class Config:
        schema_extra = {
            "example": {
                "title": "Лапчик",
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
                       example="example@mail.ru", min_length=3)


class UserCreate(UserBase):
    password: str = Field(...,
                          title="Введите пароль",
                          example="example_password", min_length=4)


class User(UserBase):
    id: int
    pets: List[Pet] = []

    class Config:
        orm_mode = True
