from typing import Iterable
from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.database import Base
from models.pets import PetModel
from models.users import UserModel
from repositories.logs import logger


# GET
def get_entries(table_name: Base,
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


# DELETE
def delete_entry(entry: Base, db: Session) -> None:
    """
    Определяет тип переданного объекта и удаляет его из базы данных
    :param entry: сама запись которую необходимо удалить
    :param db: соединение с базой данных
    :return: делает запись в лог, ничего не возвращает
    """
    if isinstance(entry, UserModel):
        db.delete(entry)
        db.commit()
        logger.info(f"Пользователь с id = {entry.id} удален")
    if isinstance(entry, PetModel):
        db.delete(entry)
        db.commit()
        logger.info(f"Питомец с id хозяина = {entry.owner_id} и id животного = {entry.id} удален")


def delete_entries(entries: Base, db: Session) -> None:
    """
    Удаляет список записей в базе данных
    :param entries: удаляемые записи
    :param db: соединение с базой данных
    :return: делает запись в лог, ничего не возвращает
    """
    for i in entries:
        delete_entry(i, db)


# Прочие функции
def checking_for_matches_in_db(entry: Base,
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


def check_for_existence_in_db(entry: Base,
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
    """
    if exception:
        if not entry:
            logger.warning(f'{status_code} {detail}')
            raise type_error(status_code=status_code, detail=detail)
    else:
        if not entry:
            logger.warning(f'{status_code} {detail}')
