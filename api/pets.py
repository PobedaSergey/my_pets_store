from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, Path, Query, APIRouter, HTTPException

from api.dependencies import get_db
from models.pets import PetModel
from repositories import crud
from repositories.logs import logger
from schemas.pets import PetCreate, PetSchemas


router_pet = APIRouter(prefix="/pet", tags=["Pet Operations"], dependencies=[Depends(get_db)])
router_pets = APIRouter(prefix="/pets", tags=["Pet Operations"], dependencies=[Depends(get_db)])


# POST
@router_pet.post("/{user_id}/")
async def create_pet_for_user(pet: PetCreate,
                              user_id: int = Path(..., description="Пользовательский id"),
                              db: Session = Depends(get_db)):
    logger.info(f'Попытка добавления питомца по кличке "{pet.animal_name}" пользователю с id = "{user_id}"')
    user = crud.get_user(user_id, db)
    crud.check_for_existence_in_db(user, f"Пользователь с id {user_id} не найден")
    all_pets_from_user = crud.get_all_pets_from_user(user_id, db)
    for users_pet in all_pets_from_user:
        if pet.animal_name == users_pet.animal_name and pet.description == users_pet.description:
            status_code, detail = 400, f"У пользователя с id {user_id} уже есть питомец с такой кличкой и описанием"
            logger.warning(f"{status_code} {detail}")
            raise HTTPException(status_code, detail)
    crud.create_user_pet(pet, user_id, db)
    return {"detail": "Питомец добавлен"}


# GET
@router_pet.get("/", response_model=PetSchemas)
async def show_pet(pet_id: int = Query(..., description="id питомца"),
                   owner_id: int = Query(..., description="Пользовательский id"),
                   db: Session = Depends(get_db)):
    logger.info(f"Попытка отобразить информацию о питомце по id хозяина = {owner_id} и id животного = {pet_id}")
    pet = crud.get_pet(owner_id, pet_id, db)
    crud.check_for_existence_in_db(pet, f"Питомец по id хозяина = {owner_id} и id животного = {pet_id} не найден")
    logger.info(f"Информация о питомце по id хозяина = {owner_id} и id животного = {pet_id} предоставлена")
    return pet


@router_pets.get("/{user_id}/")
async def show_pets_of_user(user_id: int = Path(..., description="Пользовательский id"),
                            db: Session = Depends(get_db)):
    logger.info(f"Попытка отобразить всех питомцев пользователя с id = {user_id}")
    pets_of_user = crud.get_all_pets_from_user(user_id, db)
    crud.check_for_existence_in_db(pets_of_user, f"У пользователя с id = {user_id} нет питомцев "
                                                 f"или пользователя с таким id не существует")
    logger.info(f"Информация о питомцах пользователя с id = {user_id} предоставлена")
    return pets_of_user


@router_pets.get("/", response_model=List[PetSchemas])
async def show_all_pets(skip: int = Query(0, description="Сколько записей пропустить"),
                        limit: int = Query(100, description="Максимальное число отображаемых записей"),
                        db: Session = Depends(get_db)):
    logger.info("Попытка отобразить всех питомцев в магазине")
    all_pets = crud.get_entries(PetModel, db, skip, limit)
    crud.check_for_existence_in_db(all_pets, "База данных питомцев пуста")
    logger.info("Информация о всех питомцах в магазине предоставлена")
    return all_pets


# PUT
@router_pet.put("/{pet_id}/{owner_id}/")
async def change_pet(pet_id: int = Path(..., description="id питомца"),
                     owner_id: int = Path(..., description="id пользователя"),
                     new_animal_name: str = Query(..., description="Измененная кличка"),
                     new_description: str = Query(..., description="Измененное описание"),
                     db: Session = Depends(get_db)):
    logger.info(f"Попытка изменить информацию о питомце по id хозяина = {owner_id} и id животного = {pet_id}")
    user = crud.get_user(owner_id, db)
    crud.check_for_existence_in_db(user, f"Пользователь с id {owner_id} не найден")
    user = crud.get_pet(owner_id, pet_id, db)
    crud.check_for_existence_in_db(user, f"Питомец с таким id у данного пользователя не найден")
    modified_pet = crud.get_pets_by_animal_name_and_description(new_animal_name, new_description, db)
    crud.checking_for_matches_in_db(modified_pet, "У пользователя уже есть питомец с такой кличкой и описанием")
    pet = crud.get_pet(owner_id, pet_id, db)
    crud.put_pet(pet, new_animal_name, new_description, db)
    return {"detail": "Данные питомца изменены"}


# DELETE
@router_pet.delete("/{pet_id}/{owner_id}/")
async def delete_pet(pet_id: int = Path(..., description="id питомца"),
                     owner_id: int = Path(..., description="id пользователя"),
                     db: Session = Depends(get_db)):
    logger.info(f"Попытка удаления питомца по id хозяина = {owner_id} и id животного = {pet_id}")
    pet_to_be_deleted = crud.get_pet(owner_id, pet_id, db)
    crud.check_for_existence_in_db(pet_to_be_deleted,
                                   f"Питомец с id хозяина = {owner_id} и id животного = {pet_id} не найден")
    crud.delete_entry(pet_to_be_deleted, db)
    return {"detail": "Питомец удален"}


@router_pets.delete("/{owner_id}/")
async def deleting_all_pets_from_user(owner_id: int = Path(..., description="id пользователя"),
                                      db: Session = Depends(get_db)):
    logger.info(f"Попытка удаления все питомцев у пользователя с id = {owner_id}")
    all_pets_from_user = crud.get_all_pets_from_user(owner_id, db)
    crud.check_for_existence_in_db(all_pets_from_user, f"У пользователей с id = {owner_id} нет питомцев"
                                                       f"или такого пользователя не существует")
    crud.delete_entries(all_pets_from_user, db)
    return {"detail": "Все питомцы пользователя удалены"}
