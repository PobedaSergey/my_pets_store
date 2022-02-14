from typing import Iterable
from sqlalchemy.orm import Session

from models.pets import PetModel
from repositories.logs import logger
from schemas.pets import PetCreate, PetSchemas


# POST
def create_user_pet(
        pet: PetCreate,
        user_id: int,
        db: Session
) -> PetModel:
    db_pet = PetModel(**pet.dict(), owner_id=user_id)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    logger.info(f'Питомец по кличке "{db_pet.animal_name}" добавлен пользователю с id = {user_id}')
    return db_pet


# GET
def get_pet(
        owner_id: int,
        pet_id: int,
        db: Session
) -> PetModel:
    return db.query(PetModel).filter_by(owner_id=owner_id, id=pet_id).first()


def get_pets_by_animal_name_and_description(
        animal_name: str,
        description: str,
        db: Session
) -> PetModel:
    return db.query(PetModel).filter_by(animal_name=animal_name, description=description, ).first()


def get_all_pets_from_user(user_id: int, db: Session) -> Iterable:
    return db.query(PetModel).filter_by(owner_id=user_id).all()


# PUT
def put_pet(
        pet: PetSchemas,
        new_animal_name: str,
        new_description: str,
        db: Session
) -> None:
    pet.animal_name = new_animal_name
    pet.description = new_description
    db.commit()
    db.refresh(pet)
    logger.info(f"Информация о питомце по id хозяина = {pet.owner_id} и id животного = {pet.id} изменена")
