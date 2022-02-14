from typing import Iterable
from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.database import Base
from models.pets import PetModel
from models.users import UserModel
from repositories.logs import logger


# GET
def get_entries(
        table_name: Base,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        display_all: bool = False
) -> Iterable:
    if display_all:
        return db.query(table_name).all()
    return db.query(table_name).offset(skip).limit(limit).all()


# DELETE
def delete_entry(entry: Base, db: Session) -> None:
    if isinstance(entry, UserModel):
        db.delete(entry)
        db.commit()
        logger.info(f"Пользователь с id = {entry.id} удален")
    if isinstance(entry, PetModel):
        db.delete(entry)
        db.commit()
        logger.info(f"Питомец с id хозяина = {entry.owner_id} и id животного = {entry.id} удален")


def delete_entries(entries: Base, db: Session) -> None:
    for i in entries:
        delete_entry(i, db)


# Прочие функции
def checking_for_matches_in_db(
        entry: Base,
        detail: str,
        status_code: int = 400,
        type_error=HTTPException
) -> None:
    if entry:
        logger.warning(f'{status_code} {detail}')
        raise type_error(status_code=status_code, detail=detail)


def check_for_existence_in_db(
        entry: Base,
        detail: str,
        status_code: int = 404,
        type_error=HTTPException,
        exception=True
) -> None:
    if exception:
        if not entry:
            logger.warning(f'{status_code} {detail}')
            raise type_error(status_code=status_code, detail=detail)
    else:
        if not entry:
            logger.warning(f'{status_code} {detail}')
