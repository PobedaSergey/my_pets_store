from sqlalchemy.orm import Session

from models.users import UserModel
from repositories.logs import logger
from repositories.other_functions import encrypt_password
from schemas.users import UserCreate, UserSchemas


# POST
def create_user(user: UserCreate, db: Session) -> UserModel:
    fake_hashed_password = encrypt_password(user.password)
    db_user = UserModel(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f'Пользователь c email: "{db_user.email}" и id = {db_user.id} создан')
    return db_user


# GET
def get_user(user_id: int, db: Session) -> UserModel:
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_email(email: str, db: Session) -> UserModel:
    return db.query(UserModel).filter(UserModel.email == email).first()


# PUT
def put_user(user: UserSchemas, new_email: str, db: Session) -> None:
    user.email = new_email
    db.commit()
    db.refresh(user)
    logger.info(f"Информация о пользователе с id = {user.id} изменена")
