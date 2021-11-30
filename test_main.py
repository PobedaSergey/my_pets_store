from fastapi.testclient import TestClient

from main import app
from logs import *

client = TestClient(app)


# POST
# Тестирование метода create_user
def test_creating_new_original_user(sequential_number,  email, password):
    # Параметр sequential_number не задает id создаваемых пользователей,
    # но должен им соответствовать, sequential_number должен начинаться с 1
    # и увеличиваться на 1 с созданием нового пользователя.
    response = client.post("/user/", json={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json() == {"email": email,
                               "id": sequential_number,
                               "pets": []}


def test_creating_user_with_an_email_that_already_exists_in_the_db(email, password):
    response = client.post("/user/", json={"email": email, "password": password})
    assert response.status_code == 400
    assert response.json() == {"detail": 'Пользователь с таким email уже зарегистрирован'}


# Тестирование метода create_pet_for_user
def creating_new_pet_for_user(user_id, title, description):
    response = client.post(f"/user/{user_id}/pets/", json={"title": title, "description": description})
    assert response.status_code == 200
    assert response.json() == {"detail": "Питомец добавлен"}


def creating_pet_for_user_that_does_not_exist(user_id, title, description):
    response = client.post(f"/user/{user_id}/pets/", json={"title": title, "description": description})
    assert response.status_code == 404
    assert response.json() == {"detail": f"Пользователь с id {user_id} не найден"}


def creating_pet_with_pre_existing_name_and_description(user_id, title, description):
    response = client.post(f"/user/{user_id}/pets/", json={"title": title, "description": description})
    assert response.status_code == 400
    assert response.json() == {"detail": f"У пользователя с id {user_id} уже есть питомец с такой кличкой и описанием"}


# GET
# Тестирование метода show_users
def displaying_all_users_when_db_is_not_empty(skip=0, limit=100):
    response = client.get(f"/users/?skip={skip}&limit={limit}")
    assert response.status_code == 200


def displaying_all_users_when_db_is_empty(skip=0, limit=100):
    response = client.get(f"/users/?skip={skip}&limit={limit}")
    assert response.status_code == 404
    assert response.json() == {"detail": "База данных пользователей пуста"}


# Тестирование метода show_user
def display_an_existing_user(user_id):
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200


def display_non_existent_user(user_id):
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Пользователь с id {user_id} не найден"}


# Тестирование метода show_pet
def display_pet_on_wrong_id(pet_id, owner_id):
    response = client.get(f"/pet/?pet_id={pet_id}&owner_id={owner_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Питомец по id хозяина = {owner_id} и id животного = {pet_id} не найден"}


def display_pet_by_correct_id(pet_id, owner_id):
    response = client.get(f"/pet/?pet_id={pet_id}&owner_id={owner_id}")
    assert response.status_code == 200
    assert response.json() == {"title": "test_title_1",
                               "description": "test_description_1",
                               "id": 1,
                               "owner_id": 1}


# Тестирование метода show_pets_of_user
def display_all_pets_of_user(user_id):
    response = client.get(f"/pets/{user_id}/")
    assert response.status_code == 200


def display_all_pets_of_non_existent_user(user_id):
    response = client.get(f"/pets/{user_id}/")
    assert response.status_code == 404
    assert response.json() == {"detail": f"У пользователя с id = {user_id} нет питомцев или "
                                         "пользователя с таким id не существует"}


# Тестирование метода show_all_pets
def display_all_pets_when_they_are(skip=0, limit=100):
    response = client.get(f"/pets/?skip={skip}&limit={limit}")
    assert response.status_code == 200


def display_all_pets_when_there_are_none(skip=0, limit=100):
    response = client.get(f"/pets/?skip={skip}&limit={limit}")
    assert response.status_code == 404
    assert response.json() == {"detail": "База данных питомцев пуста"}


# PUT
# Тестирование метода change_user_by_id
def changing_the_email_of_user_that_does_not_exist_in_db(user_id, new_email):
    response = client.put(f"/user/{user_id}/?new_email={new_email}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Пользователь с id {user_id} не найден"}


def changing_the_user_email_to_an_existing_one_in_db(user_id, new_email):
    response = client.put(f"/user/{user_id}/?new_email={new_email}")
    assert response.status_code == 400
    assert response.json() == {"detail": f"Пользователь с email: {new_email} уже зарегистрирован"}


def change_email_to_user(user_id, new_email):
    response = client.put(f"/user/{user_id}/?new_email={new_email}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Электронная почта пользователя изменена"}


# Тестирование метода change_pets
def changing_non_existent_pet(pet_id, owner_id, new_title, new_description):
    response = client.put(f"/user/{pet_id}/"
                          f"{owner_id}/?"
                          f"new_title={new_title}/&"
                          f"new_description={new_description}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Пользователь с id {owner_id} не найден"}


def pet_change_by_nonexistent_owner(pet_id, owner_id, new_title, new_description):
    response = client.put(f"/user/{pet_id}/"
                          f"{owner_id}/?"
                          f"new_title={new_title}/&"
                          f"new_description={new_description}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Питомец с таким id у данного пользователя не найден"}


def changing_pet_data_to_existing_ones_for_the_user(pet_id, owner_id, new_title, new_description):
    response = client.put(f"/user/{pet_id}/"
                          f"{owner_id}/?"
                          f"new_title={new_title}/&"
                          f"new_description={new_description}")
    assert response.status_code == 400
    assert response.json() == {"detail": "У пользователя уже есть питомец с такой кличкой и описанием"}


def changing_pet_data(pet_id, owner_id, new_title, new_description):
    response = client.put(f"/user/{pet_id}/"
                          f"{owner_id}/?"
                          f"new_title={new_title}/&"
                          f"new_description={new_description}")
    assert response.status_code == 200
    assert {"detail": "Данные питомца изменены"}


# DELETE
# Тестирование метода delete_user
def deleting_non_existent_user(user_id):
    response = client.delete(f"/user/{user_id}/")
    assert response.status_code == 404
    assert {"detail": f"Пользователь с id = {user_id} не найден"}


def deleting_user(user_id):
    response = client.delete(f"/user/{user_id}/")
    assert response.status_code == 200
    assert {"detail": "Пользователь удален"}


# Тестирование метода delete_pet
def deleting_pet_for_wrong_id(pet_id, owner_id):
    response = client.delete(f"/pet/{pet_id}/{owner_id}/")
    assert response.status_code == 404
    assert {"detail": f"Питомец с id хозяина = {owner_id} и id животного = {pet_id} не найден"}


def deleting_pet(pet_id, owner_id):
    response = client.delete(f"/pet/{pet_id}/{owner_id}/")
    assert response.status_code == 200
    assert {"detail": "Питомец удален"}


# Тестирование метода deleting_all_pets_from_user
def deleting_all_pets_from_the_user_by_wrong(user_id):
    response = client.delete(f"/pets/{user_id}/")
    assert response.status_code == 404
    assert {"detail": f"У пользователей с id = {user_id} нет питомцев "
                      f"или такого пользователя не существует"}


def deleting_all_pets_from_the_user(user_id):
    response = client.delete(f"/pets/{user_id}/")
    assert response.status_code == 200
    assert {"detail": "Все питомцы пользователя удалены"}


# Тестирование метода delete_all_users
def deleting_all_users_in_an_empty_db():
    response = client.delete("/users/")
    assert response.status_code == 404
    assert {"detail": "База данных пользователей пуста"}


def deleting_all_users_in_db():
    response = client.delete("/users/")
    assert response.status_code == 200
    assert {"detail": "Все пользователи удалены"}


# Удаление всех пользователей
def deleting_all():
    response = client.delete("/users/")


if __name__ == '__main__':
    logger.info("Начато тестирование модуля main")
    # полная очистка базы
    deleting_all()
    # создаем оригинального пользователя
    test_creating_new_original_user(1, "test_email_1@mail.ru", "test_password")
    # создаем пользователя с таким же email
    test_creating_user_with_an_email_that_already_exists_in_the_db("test_email_1@mail.ru", "test_password")
    # создаем ему питомца
    creating_new_pet_for_user(1, "test_title_1", "test_description_1")
    # создаем питомца с таким же описанием
    creating_pet_with_pre_existing_name_and_description(1, "test_title_1", "test_description_1")
    # создаем питомца несуществующему пользователю
    creating_pet_for_user_that_does_not_exist(99, "test_title", "test_description")
    # получаем информацию о существующем пользователе
    display_an_existing_user(1)
    # получаем информацию о не существующем пользователе
    display_non_existent_user(88)
    # получаем информацию о питомце по неправильному id хозяина
    display_pet_on_wrong_id(77, 1)
    # получаем информацию о питомце по неправильному id питомца
    display_pet_on_wrong_id(1, 66)
    # получаем информацию по корректным id
    display_pet_by_correct_id(1, 1)
    # создаем еще одного питомца первому пользователю
    creating_new_pet_for_user(1, "test_title_2", "test_description_2")
    # получаем список его питомцев
    display_all_pets_of_user(1)
    # получаем питомцев по неправильному id пользователя
    display_all_pets_of_non_existent_user(55)
    # создаем второго пользователя
    test_creating_new_original_user(2, "test_email_2@mail.ru", "test_password")
    # создаем питомца второму пользователю
    creating_new_pet_for_user(2, "test_title_2", "test_description_2")
    # получаем список всех питомцев в магазине
    display_all_pets_when_they_are()
    # первому пользователю меняем email
    change_email_to_user(1, "new_test_email_1@mail.ru")
    # второму меняем email на такой же как у первого
    changing_the_user_email_to_an_existing_one_in_db(2, "new_test_email_1@mail.ru")
    # меняем почту несуществующему пользователю
    changing_the_email_of_user_that_does_not_exist_in_db(33, "test_email")
    # редактируем питомца несуществующего пользователя
    pet_change_by_nonexistent_owner(77, 1, "new_title", "new_description")
    # редактируем несуществующего питомца пользователя
    changing_non_existent_pet(1, 77, "new_title", "new_description")
    # редактируем описание питомца первого пользователя
    changing_pet_data(1, 1, "new_test_title_1", "new_test_description_1")
    # редактируем описание питомца первого пользователя на такое же
    changing_pet_data_to_existing_ones_for_the_user(2, 1, "new_test_title_1", "new_test_description_1")
    # удаляем всех питомцев первого пользователя
    deleting_all_pets_from_the_user(1)
    # удаляем питомца второго пользователя
    deleting_pet(3, 2)
    # пытаемя удалить несуществующего питомца по id хозяина
    deleting_pet_for_wrong_id(77, 1)
    # пытаемся удалить питомца у несуществующего пользователя
    deleting_pet_for_wrong_id(1, 77)
    # пытаемся удалить всех питомцев у пользователя у которого нет питомцев
    deleting_all_pets_from_the_user_by_wrong(1)
    # пытаемся удалить всех питомцев у несуществующего пользователя
    deleting_all_pets_from_the_user_by_wrong(55)
    # Удаляем несуществующего пользователя
    deleting_non_existent_user(55)
    # удаляем существующего пользователя
    deleting_user(1)
    # удаляем всех пользователей
    deleting_all_users_in_db()
    # удаляем пользователей из пустой базы
    deleting_all_users_in_an_empty_db()
    # создаем пользователя
    test_creating_new_original_user(1, "test_email_3@mail.ru", "test_password")
    # отображаем питомцев пользователя у которого нет питомцев
    display_all_pets_when_there_are_none(1)
    # очищаем базу
    deleting_all_users_in_db()
    logger.info("Тестирование модуля main успешно завершено")





