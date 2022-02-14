from pydantic import Field

from schemas.base_schemas import ModBaseModel


class PetBase(ModBaseModel):
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


class PetSchemas(PetBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
