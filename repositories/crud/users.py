from sqlalchemy.orm import Session

from models.users import UserModel
from repositories.logs import logger
from repositories.other_functions import encrypt_password
from schemas.users import UserCreate, UserSchemas


# POST
def create_user(user: UserCreate, db: Session) -> UserModel:
    """
    Создает нового пользователя, хеширует пароль.
    :param db: соединение с базой данных
    :param user: схема создания объекта
    :return: только что созданную строчку в UserModel
    """
    fake_hashed_password = encrypt_password(user.password)
    db_user = UserModel(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f'Пользователь c email: "{db_user.email}" и id = {db_user.id} создан')
    return db_user


# GET
def get_user(user_id: int, db: Session) -> UserModel:
    """
    Возвращает информацию о пользователе по его id
    :param user_id: id по которому будет производится поиск
    :param db: соединение с базой данных
    :return: запись в UserModel соответствующую указанному id
    """
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_email(email: str, db: Session) -> UserModel:
    """
    Возвращает информацию о пользователе по его email
    :param email: email по которому будет искать
    :param db: соединение с базой данных
    :return: запись в UserModel соответствующую указанному email
    """
    return db.query(UserModel).filter(UserModel.email == email).first()


# PUT
def put_user(user: UserSchemas, new_email: str, db: Session) -> None:
    """
    Изменяет данные пользователя в базе данных
    :param user: сам изменяемый объект
    :param new_email: измененный email
    :param db: соединение с базой данных
    :return: ничего не возвращает
    """
    user.email = new_email
    db.commit()
    db.refresh(user)
    logger.info(f"Информация о пользователе с id = {user.id} изменена")
