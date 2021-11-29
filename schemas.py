from pydantic import BaseModel
from typing import List, Optional


# Родительский класс содержащий инфу о питомце
# class ItemBase(BaseModel):
class PetBase(BaseModel):
    title: str
    description: Optional[str] = None


# Через этот класс необходимо реализовать добавление нового питомца
# class ItemCreate(ItemBase):
class PetCreate(PetBase):
    pass


# Содержит id животного и id его хозяина, также настройки конфигурации
# (Config стоит еще уточнить)
# class Item(ItemBase):
class Pet(PetBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Родительский класс для пользователя
class UserBase(BaseModel):
    email: str


# Сделан для того чтобы при создании пользователя
# получить от него пароль, но больше нигде его не светить.
class UserCreate(UserBase):
    password: str


# Содержит id пользователя и список его питомцев,
# также настройки конфигурации (Config стоит еще уточнить)
class User(UserBase):
    id: int
    pets: List[Pet] = []

    class Config:
        orm_mode = True
