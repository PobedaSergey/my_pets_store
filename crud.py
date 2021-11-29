from typing import Optional, List, Any, Iterable
from sqlalchemy.orm import Session
from fastapi import FastAPI, Query, Depends, HTTPException


import schemas
import models
from logs import *


# POST
def create_user(user: schemas.UserCreate, db: Session) -> models.User:
    """
    Создает нового пользователя, хеширует пароль.
    :param db: соединение с базой данных
    :param user: схема создания объекта
    :return: только что созданную строчку в models.User
    """
    fake_hashed_password = encrypt_password(user.password)
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f'Пользователь c email: "{db_user.email}" и id = {db_user.id} создан')
    return db_user


def create_user_pet(pet: schemas.PetCreate, user_id: int, db: Session) -> models.Pet:
    """
    Создает нового питомца, привязанного к пользователю.
    :param pet: схема создания объекта
    :param user_id: id пользовтеля к которому будет привязан питомец
    :param db: соединение с базой данных
    :return: только что созданную строчку в models.Pet
    """
    db_pet = models.Pet(**pet.dict(), owner_id=user_id)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    logger.info(f'Питомец по кличке "{db_pet.title}" добавлен пользователю с id = {user_id}')
    return db_pet


# GET
def get_user(user_id: int, db: Session) -> models.User:
    """
    Возвращает информацию о пользователе по его id
    :param user_id: id по которому будет производится поиск
    :param db: соединение с базой данных
    :return: запись в models.User соответствующую указанному id
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(email: str, db: Session) -> models.User:
    """
    Возвращает информацию о пользователе по его email
    :param email: email по которому будет искать
    :param db: соединение с базой данных
    :return: запись в models.User соответствующую указанному email
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_pet(owner_id: int, pet_id: int, db: Session) -> models.Pet:
    """
    Возвращает информацию о питомце по указанному id его хозяиина
    :param owner_id: id пользователя за которым закреплен питомец
    :param pet_id: id питомца
    :param db: соединение с базой данных
    :return: запись в models.Pet соответствующую указанному owner_id
    """
    return db.query(models.Pet).filter_by(owner_id=owner_id, id=pet_id).first()


def get_pets_by_title_and_description(title: str, description: str, db: Session) -> models.Pet:
    """
    Возвращает информацию о питомце по указанному описанию и имени
    :param title: имя питомца
    :param description: его описание
    :param db: соединение с базой данных
    :return: запись в models.Pet соответствующую указанным параметрам
    """
    return db.query(models.Pet).filter_by(title=title, description=description,).first()


def get_all_pets_from_user(user_id: int, db: Session) -> Iterable:
    """
    Возвращает записи обо всех питомцах данного пользователя
    :param user_id: id пользователя
    :param db: соединение с базой данных
    :return: все записи в models.Pet по указанному id пользователя
    """
    return db.query(models.Pet).filter_by(owner_id=user_id).all()


def get_entries(table_name: models.Base,
                db: Session,
                skip: int = 0,
                limit: int = 100,
                display_all: bool = False) -> Iterable:
    """
    Возвращает диапазон или все записи из базы данных
    :param table_name: имя таблицы из которой будет полученна информация
    :param db: соединение с базой данных
    :param skip: задает число записей которые будут пропущены
    :param limit: задает максимальное колличество записей
    :param display_all: если включен, то функция вернет все значения из базы данных
    :return: записи из указанной базы данных, без фильтрации
    """
    if display_all:
        return db.query(table_name).all()
    return db.query(table_name).offset(skip).limit(limit).all()


# PUT
def put_user(user: schemas.User, new_email: str, db: Session) -> None:
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


def put_pet(pet: schemas.Pet,
            new_title: str,
            new_description: str,
            db: Session) -> None:
    """
    Изменяет данные питомца в базе данных
    :param pet: сам изменяемый объект
    :param new_title: новое имя питомца
    :param new_description: новое описание
    :param db: соединение с базой данных
    :return: ничего не возвращает
    """
    pet.title = new_title
    pet.description = new_description
    db.commit()
    db.refresh(pet)
    logger.info(f"Информация о питомце по id хозяина = {pet.owner_id} и id животного = {pet.id} изменена")


# DELETE
def delete_entry(entry: models.Base, db: Session) -> None:
    """
    Определяет тип переданного объекта и удаляет его из базы данных
    :param entry: сама запись которую необходимо удалить
    :param db: соединение с базой данных
    :return: делает запись в лог, ничего не возвращает
    """
    if isinstance(entry, models.User):
        db.delete(entry)
        db.commit()
        logger.info(f"Пользователь с id = {entry.id} удален")
    if isinstance(entry, models.Pet):
        db.delete(entry)
        db.commit()
        logger.info(f"Питомец с id хозяина = {entry.owner_id} и id животного = {entry.id} удален")


def delete_entries(entries: models.Base, db: Session) -> None:
    """
    Удаляет список записей в базе данных
    :param entries: удаляемые записи
    :param db: соединение с базой данных
    :return: делает запись в лог, ничего не возвращает
    """
    for i in entries:
        delete_entry(i, db)


# Прочие функции
def encrypt_password(password: str) -> str:
    """
    Имитирует хеширование пароля.
    """
    return password + "abracadabra"


def checking_for_matches_in_db(entry: models.Base,
                               detail: str,
                               status_code: int = 400,
                               type_error=HTTPException) -> None:
    """
    Проверяет совпадение этой записи с теми, что уже занесены в базу данных
    :param entry: база данных в которой проводится проверка
    :param detail: текст который будет выведен в случае существования записи
    :param status_code: код исколючения
    :param type_error: тип исключения
    :return: исключение если запись найдена в противном случае не возвращает ничего
    """
    if entry:
        logger.warning(f'{status_code} {detail}')
        raise type_error(status_code=status_code, detail=detail)


def check_for_existence_in_db(entry: models.Base,
                              detail: str,
                              status_code: int = 404,
                              type_error=HTTPException,
                              exception=True) -> None:
    """
    Проверяет существование записи в базе данных
    :param entry: база данных в которой проводится проверка
    :param detail: текст который будет выведен в случае существования записи
    :param status_code: код исколючения
    :param type_error: тип исключения
    :param exception: если True то выбрасывает исключение и пишет об этом в лог,
                      если False то просто пишет ифнормацию в лог
    :return: пишет в лог, если записи в базе нет, опционально выбрасывает исключение
             если проверка пройдена успешно, выполняет функцию func
    """
    if exception:
        if not entry:
            logger.warning(f'{status_code} {detail}')
            raise type_error(status_code=status_code, detail=detail)
    else:
        if not entry:
            logger.warning(f'{status_code} {detail}')


