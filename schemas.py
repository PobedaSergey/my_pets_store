from pydantic import BaseModel
from typing import List, Optional


class PetBase(BaseModel):
    title: str
    description: Optional[str] = None


class PetCreate(PetBase):
    pass


class Pet(PetBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    pets: List[Pet] = []

    class Config:
        orm_mode = True
