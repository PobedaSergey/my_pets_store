import uvicorn
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Тестовое API",
    description="Вторая версия приложения, данные лежат в SQLite",
    version="0.0.2",
    license_info={
        "name": "Допустим под лицензией Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


# tags_metadata = [{"name": "user"}, {"name": "users"}]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Запросы POST
@app.post("/user/", response_model=schemas.User, tags=["Users"])
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/user/{user_id}/pets/", response_model=schemas.Pet, tags=["Pets"])
async def create_pet_for_user(user_id: int, pet: schemas.PetCreate, db: Session = Depends(get_db)):
    return crud.create_user_pet(db=db, pet=pet, user_id=user_id)


# Запросы GET
# TODO добавить ответ
@app.get("/users/", response_model=List[schemas.User], tags=["Users"])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/user/{user_id}", response_model=schemas.User, tags=["Users"])
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# TODO добавить ответ
@app.get("/pets/", response_model=List[schemas.Pet], tags=["Pets"])
async def read_pets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pets = crud.get_pets(db, skip=skip, limit=limit)
    return pets


# TODO добавить ответ
@app.get("/pet/", response_model=schemas.Pet, tags=["Pets"])
async def read_pet(id: int, owner_id: int, db: Session = Depends(get_db)):
    pet = crud.get_pet(owner_id=owner_id, id=id, db=db)
    return pet


# Запросы PUT
# TODO добавить ответ, а также совпадения по почте
@app.put("/user/{user_id}", tags=["Users"])
async def change_user_by_id(user_id: int, new_email: str, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    crud.put_user(db=db, user=user, new_email=new_email)
    return "Ok"


# TODO добавить ответ, а также совпадения по почте
@app.put("/user/{user_id}/{owner_id}", tags=["Pets"])
async def change_pets(id: int, owner_id: int, new_title: str, new_description: str, db: Session = Depends(get_db)):
    pet = crud.get_pet(db=db, id=id, owner_id=owner_id)
    crud.put_pet(db=db, pet=pet, new_title=new_title, new_description=new_description)
    return "Ok"


# Запросы DELETE
@app.delete("/user/{user_id}", tags=["Users"])
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    all_pets_from_user = crud.get_all_pets_from_user(owner_id=user_id, db=db)
    if all_pets_from_user is not None:
        for i in all_pets_from_user:
            crud.delete_user(db, i)

    user_to_be_deleted = crud.get_user(db, user_id=user_id)
    if user_to_be_deleted is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_to_be_deleted)
    return "User deleted"


@app.delete("/pet/{user_id}/{pet_id}", tags=["Pets"])
async def delete_pet(owner_id: int, pet_id: int, db: Session = Depends(get_db)):
    pet_to_be_deleted = crud.get_pet(id=pet_id, owner_id=owner_id, db=db)
    if pet_to_be_deleted is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    crud.delete_pet(db, pet_to_be_deleted)
    return "Pet deleted"


@app.delete("/pets/{owner_id}/", tags=["Pets"])
async def deleting_all_pets_from_user(owner_id: int, db: Session = Depends(get_db)):
    all_pets_from_user = crud.get_all_pets_from_user(owner_id=owner_id, db=db)
    if all_pets_from_user is None:
        raise HTTPException(status_code=404, detail="User has no pets")
    for i in all_pets_from_user:
        crud.delete_user(db, i)
    return "All pets for this user have been deleted "


@app.delete("/users/", tags=["Users"])
async def delete_all_users(db: Session = Depends(get_db)):
    all_users = crud.get_all_users(db)
    if all_users is None:
        raise HTTPException(status_code=404, detail="User database is empty")
    for i in all_users:
        all_pets_from_user = crud.get_all_pets_from_user(owner_id=i.id, db=db)
        if all_pets_from_user is not None:
            for j in all_pets_from_user:
                crud.delete_user(db, j)
        user_to_be_deleted = crud.get_user(db, user_id=i.id)
        if user_to_be_deleted is not None:
            crud.delete_user(db, user_to_be_deleted)
    return "User database cleared"


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8004)
