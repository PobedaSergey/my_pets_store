from typing import Iterable
from sqlalchemy.orm import Session

from models.pets import PetModel
from repositories.logs import logger
from schemas.pets import PetCreate, PetSchemas


# POST
def create_user_pet(pet: PetCreate, user_id: int, db: Session) -> PetModel:
    """
    Создает нового питомца, привязанного к пользователю.
    :param pet: схема создания объекта
    :param user_id: id пользовтеля к которому будет привязан питомец
    :param db: соединение с базой данных
    :return: только что созданную строчку в PetModel
    """
    db_pet = PetModel(**pet.dict(), owner_id=user_id)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    logger.info(f'Питомец по кличке "{db_pet.animal_name}" добавлен пользователю с id = {user_id}')
    return db_pet


# GET
def get_pet(owner_id: int, pet_id: int, db: Session) -> PetModel:
    """
    Возвращает информацию о питомце по указанному id его хозяиина
    :param owner_id: id пользователя за которым закреплен питомец
    :param pet_id: id питомца
    :param db: соединение с базой данных
    :return: запись в PetModel соответствующую указанному owner_id
    """
    return db.query(PetModel).filter_by(owner_id=owner_id, id=pet_id).first()


def get_pets_by_animal_name_and_description(animal_name: str, description: str, db: Session) -> PetModel:
    """
    Возвращает информацию о питомце по указанному описанию и имени
    :param animal_name: имя питомца
    :param description: его описание
    :param db: соединение с базой данных
    :return: запись в PetModel соответствующую указанным параметрам
    """
    return db.query(PetModel).filter_by(animal_name=animal_name, description=description, ).first()


def get_all_pets_from_user(user_id: int, db: Session) -> Iterable:
    """
    Возвращает записи обо всех питомцах данного пользователя
    :param user_id: id пользователя
    :param db: соединение с базой данных
    :return: все записи в PetModel по указанному id пользователя
    """
    return db.query(PetModel).filter_by(owner_id=user_id).all()


# PUT
def put_pet(pet: PetSchemas,
            new_animal_name: str,
            new_description: str,
            db: Session) -> None:
    """
    Изменяет данные питомца в базе данных
    :param pet: сам изменяемый объект
    :param new_animal_name: новое имя питомца
    :param new_description: новое описание
    :param db: соединение с базой данных
    :return: ничего не возвращает
    """
    pet.animal_name = new_animal_name
    pet.description = new_description
    db.commit()
    db.refresh(pet)
    logger.info(f"Информация о питомце по id хозяина = {pet.owner_id} и id животного = {pet.id} изменена")
