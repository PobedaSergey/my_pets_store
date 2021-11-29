import uvicorn
from typing import Optional, List
from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from . import crud, models, schemas, logger
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Тестовое API",
    description="Третья версия приложения, данные лежат в SQLite",
    version="0.0.3",
    license_info={
        "name": "Допустим под лицензией Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# POST
@app.post("/user/", response_model=schemas.User, tags=["Users"])
async def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f'Попытка создать пользователя с email: "{new_user.email}"')
    user_by_new_email = crud.get_user_by_email(new_user.email, db)
    crud.checking_for_matches_in_db(user_by_new_email, "Пользователь с таким email уже зарегистрирован")
    return crud.create_user(new_user, db)


@app.post("/user/{user_id}/pets/", tags=["Pets"])
async def create_pet_for_user(user_id: int,
                              pet: schemas.PetCreate,
                              db: Session = Depends(get_db)):
    logger.info(f'Попытка создания питомца по кличке "{pet.title}"')
    user = crud.get_user(user_id, db)
    crud.check_for_existence_in_db(user, "Пользователь не найден")
    all_pets_from_user = crud.get_all_pets_from_user(user_id, db)
    for users_pet in all_pets_from_user:
        if pet.title == users_pet.title and pet.description == users_pet.description:
            status_code, detail = 400, "У пользователя уже есть питомец с такой кличкой и описанием"
            logger.warning(f"{status_code} {detail}")
            raise HTTPException(status_code, detail)
    crud.create_user_pet(pet, user_id, db)
    return {"detail": "Питомец добавлен"}


# GET
@app.get("/users/", response_model=List[schemas.User], tags=["Users"])
async def show_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_entries(models.User, db, skip, limit)
    crud.check_for_existence_in_db(users, "База данных пользователей пуста")
    logger.info("Информация о пользователях предоставлена")
    return users


@app.get("/user/{user_id}", response_model=schemas.User, tags=["Users"])
async def show_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(user_id, db)
    crud.check_for_existence_in_db(user, "Пользователь не найден")
    return user


@app.get("/pet/", response_model=schemas.Pet, tags=["Pets"])
async def show_pet(pet_id: int, owner_id: int, db: Session = Depends(get_db)):
    pet = crud.get_pet(owner_id, pet_id, db)
    crud.check_for_existence_in_db(pet, "Питомец не найден")
    return pet


@app.get("/pets/{user_id}/", tags=["Pets"])
async def show_pets_of_user(user_id: int, db: Session = Depends(get_db)):
    pets_of_user = crud.get_all_pets_from_user(user_id, db)
    crud.check_for_existence_in_db(pets_of_user, "У пользователя нет питомцев")
    return pets_of_user


@app.get("/pets/", response_model=List[schemas.Pet], tags=["Pets"])
async def show_all_pets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_pets = crud.get_entries(models.Pet, db, skip, limit)
    crud.check_for_existence_in_db(all_pets, "База данных питомцев пуста")
    return all_pets


# PUT
@app.put("/user/{user_id}", tags=["Users"])
async def change_user_by_id(user_id: int, new_email: str,  db: Session = Depends(get_db)):
    user_with_the_same_email = crud.get_user_by_email(new_email, db)
    crud.checking_for_matches_in_db(user_with_the_same_email, "Пользователь с таким email уже зарегистрирован")
    user = crud.get_user(user_id, db)
    crud.put_user(user, new_email, db)
    return {"detail": "User email changed"}


@app.put("/user/{user_id}/{owner_id}", tags=["Pets"])
async def change_pets(pet_id: int,
                      owner_id: int,
                      new_title: str,
                      new_description: str,
                      db: Session = Depends(get_db)):
    modified_pet = crud.get_pets_by_title_and_description(new_title, new_description, db)
    crud.checking_for_matches_in_db(modified_pet,
                                    "У пользователя уже есть питомец с такой кличкой и описанием")
    pet = crud.get_pet(owner_id, pet_id, db)
    crud.put_pet(pet, new_title, new_description, db)
    return {"detail": "Pet description and title changed"}


# DELETE
@app.delete("/user/{user_id}", tags=["Users"])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    all_pets_from_user = crud.get_all_pets_from_user(user_id, db)
    if all_pets_from_user is not None:
        crud.delete_entries(all_pets_from_user, db)
    user_to_be_deleted = crud.get_user(user_id, db)
    crud.check_for_existence_in_db(user_to_be_deleted, "Пользователь не найден")
    crud.delete_entry(user_to_be_deleted, db)
    return {"detail": "User deleted"}


@app.delete("/pet/{user_id}/{pet_id}", tags=["Pets"])
async def delete_pet(owner_id: int, pet_id: int, db: Session = Depends(get_db)):
    pet_to_be_deleted = crud.get_pet(owner_id, pet_id, db)
    crud.check_for_existence_in_db(pet_to_be_deleted, "Питомец не найден")
    crud.delete_entry(pet_to_be_deleted, db)
    return {"detail": "Pet deleted"}


@app.delete("/pets/{owner_id}/", tags=["Pets"])
async def deleting_all_pets_from_user(owner_id: int, db: Session = Depends(get_db)):
    all_pets_from_user = crud.get_all_pets_from_user(owner_id, db)
    crud.check_for_existence_in_db(all_pets_from_user, "У пользователей нет питомцев")
    crud.delete_entries(all_pets_from_user, db)
    return {"detail": "All pets for this user have been deleted"}


@app.delete("/users/", tags=["Users"])
async def delete_all_users(db: Session = Depends(get_db)):
    all_pets = crud.get_entries(models.Pet, db, display_all=True)
    crud.check_for_existence_in_db(all_pets, "База данных питомцев пуста", exception=False)
    crud.delete_entries(all_pets, db)
    all_users = crud.get_entries(models.User, db, display_all=True)
    crud.check_for_existence_in_db(all_users, "База данных пользователей пуста")
    crud.delete_entries(all_users, db)
    return {"detail": "User database cleared"}



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8006)
