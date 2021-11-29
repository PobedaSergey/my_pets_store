import pickle
from typing import Optional

import my_class


def load_data() -> dict:
    """
    Открывает файл в котором записаны данные пользователей.
    :return: возвращает словарь с инфрмацией о пользователях.
    """
    FILENAME = 'my_mini_db.dat'
    try:
        input_file = open(FILENAME, 'rb')
        users_dct = pickle.load(input_file)
        input_file.close()
    except IOError:
        users_dct = {}
    return users_dct


def save_data(users_dct: dict) -> None:
    """
    Сохраняет изменения в файле и закрывает его.
    :param users_dct: словарь изменения в котором необходимо сохранить
    :return: ничего не возвращает
    """
    FILENAME = 'my_mini_db.dat'
    output_file = open(FILENAME, 'wb')
    pickle.dump(users_dct, output_file)
    output_file.close()


def add_user(users_dct: dict, username: Optional[str], firstname: str, phone: int) -> str:
    """
    Добавляет пользователя в словарь.
    :param users_dct: словарь в который добавляется информация
    :param username: никнейм пользователя
    :param firstname: имя пользователя
    :param phone: телефонный номер пользователя
    :return: строку с текстом сообщающую добавлися ли новый
    пользователь или пользоваетль с таким именем уже существует
    """
    user = my_class.User()
    user.firstname = firstname
    user.phone = phone
    if username not in users_dct:
        users_dct[username] = user
        my_message = 'Пользователь добавлен.'
    else:
        my_message = 'Это имя уже существует!'
    return my_message


def delete_user(users_dct: dict, username: str) -> str:
    """
    Производит поиск пользователя в словаре и удаляет его если такой есть
    :param users_dct: словарь из которого происходит удаление
    :param username: никнейм удаляемого пользователя
    :return: строку с текстом сообщающую удалился ли
    пользователь или пользователя с таким имененем не существует
    """
    if username in users_dct:
        del users_dct[username]
        my_message = 'Запись удалена.'
    else:
        my_message = 'Это имя не найдено.'
    return my_message


def delete_all_user() -> str:
    """
    Очищает словарь.
    :return: строку с текстом что словарь пуст
    """
    save_data({})
    return "Словарь полностью очищен."