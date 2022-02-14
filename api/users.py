from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, Path, Query, APIRouter

from api.dependencies import get_db
from models.users import UserModel
from models.pets import PetModel
from repositories import crud
from repositories.logs import logger
from schemas.users import UserCreate, UserSchemas


router_user = APIRouter(prefix="/user", tags=["Operations with users"], dependencies=[Depends(get_db)])
router_users = APIRouter(prefix="/users", tags=["Operations with users"], dependencies=[Depends(get_db)])


# POST
@router_user.post("/", response_model=UserSchemas)
async def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f'Попытка создать пользователя с email: "{new_user.email}"')
    user_by_new_email = crud.get_user_by_email(new_user.email, db)
    crud.checking_for_matches_in_db(user_by_new_email, "Пользователь с таким email уже зарегистрирован")
    return crud.create_user(new_user, db)


# GET
@router_users.get("/", response_model=List[UserSchemas])
async def show_users(
        skip: int = Query(0, description="Сколько записей пропустить"),
        limit: int = Query(100, description="Максимальное число отображаемых записей"),
        db: Session = Depends(get_db)
):
    logger.info("Попытка отобразить всех пользователей")
    users = crud.get_entries(UserModel, db, skip, limit)
    crud.check_for_existence_in_db(users, "База данных пользователей пуста")
    logger.info("Информация о пользователях предоставлена")
    return users


@router_user.get("/{user_id}/", response_model=UserSchemas)
async def show_user(
        user_id: int = Path(..., description="Пользовательский id"),
        db: Session = Depends(get_db)
):
    logger.info(f"Попытка отобразить пользователя с id = {user_id}")
    user = crud.get_user(user_id, db)
    crud.check_for_existence_in_db(user, f"Пользователь с id {user_id} не найден")
    logger.info(f"Информация о пользователе с id = {user_id} предоставлена")
    return user


# PUT
@router_user.put("/{user_id}/")
async def change_user_by_id(
        user_id: int = Path(..., description="Пользовательский id"),
        new_email: str = Query(..., description="Новый email"),
        db: Session = Depends(get_db)
):
    logger.info(f"Попытка изменить информацию о пользователе с id = {user_id}")
    user = crud.get_user(user_id, db)
    crud.check_for_existence_in_db(user, f"Пользователь с id {user_id} не найден")
    user_with_the_same_email = crud.get_user_by_email(new_email, db)
    crud.checking_for_matches_in_db(user_with_the_same_email, f"Пользователь с email: {new_email} уже зарегистрирован")
    user = crud.get_user(user_id, db)
    crud.put_user(user, new_email, db)
    return {"detail": "Электронная почта пользователя изменена"}


# DELETE
@router_user.delete("/{user_id}/")
async def delete_user(
        user_id: int = Path(..., description="id удаляемого пользователя"),
        db: Session = Depends(get_db)
):
    logger.info(f"Попытка удаления пользователя с id = {user_id}")
    all_pets_from_user = crud.get_all_pets_from_user(user_id, db)
    crud.delete_entries(all_pets_from_user, db)
    user_to_be_deleted = crud.get_user(user_id, db)
    crud.check_for_existence_in_db(user_to_be_deleted, f"Пользователь с id = {user_id} не найден")
    crud.delete_entry(user_to_be_deleted, db)
    return {"detail": "Пользователь удален"}


@router_users.delete("/")
async def delete_all_users(db: Session = Depends(get_db)):
    logger.info("Попытка очистки базы данных пользователей")
    all_pets = crud.get_entries(PetModel, db, display_all=True)
    crud.check_for_existence_in_db(all_pets, "База данных питомцев пуста", exception=False)
    crud.delete_entries(all_pets, db)
    all_users = crud.get_entries(UserModel, db, display_all=True)
    crud.check_for_existence_in_db(all_users, "База данных пользователей пуста")
    crud.delete_entries(all_users, db)
    return {"detail": "Все пользователи удалены"}
