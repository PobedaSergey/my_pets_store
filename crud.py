import pickle
from typing import Optional
from sqlalchemy.orm import Session

from ver2_db import schemas, models


# Функции POST
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_pet(db: Session, pet: schemas.PetCreate, user_id: int):
    db_pet = models.Pet(**pet.dict(), owner_id=user_id)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


# Функции GET
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_pet(id: int, owner_id: int, db: Session):
    return db.query(models.Pet).filter_by(owner_id=owner_id, id=id).first()


# TODO Объединить две нижних?
def get_pets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pet).offset(skip).limit(limit).all()


def get_all_pets(db: Session):
    return db.query(models.Pet).all()


def get_all_users(db: Session):
    return db.query(models.User).all()


def get_all_pets_from_user(owner_id: int, db: Session):
    return db.query(models.Pet).filter_by(owner_id=owner_id).all()


# Функции PUT
def put_user(db: Session, user, new_email):
    user.email = new_email
    db.commit()
    db.refresh(user)


def put_pet(db: Session, pet, new_title, new_description):
    pet.title = new_title
    pet.description = new_description
    db.commit()
    db.refresh(pet)


# Функции DELETE
# TODO объединить лишние функции удаления в одну
def delete_user(db: Session, user_to_be_deleted):
    db.delete(user_to_be_deleted)
    db.commit()


def delete_pet(db: Session, pet_to_be_deleted):
    db.delete(pet_to_be_deleted)
    db.commit()


def delete_all_pets(db: Session, all_pets):
    db.delete(all_pets)
    db.commit()


def delete_all_users(db: Session, all_users):
    db.delete(all_users)
    db.commit()


def delete_entry(one_entry, db: Session):
    db.delete(one_entry)
    db.commit()