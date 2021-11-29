import uvicorn
from typing import Optional
from fastapi import FastAPI, Query

import my_mini_db


app = FastAPI(
    title="Тестовое API",
    description="Первая версия приложения, хранилищем данных выступает словарь.",
    version="0.0.1",
    license_info={
        "name": "Допустим под лицензией Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

tags_metadata = [{"name": "user"}, {"name": "users"}]


@app.post("/user", tags=["user"])
async def create_user(username: Optional[str] = Query(..., min_length=2, description="Никнейм."),
                      firstname: Optional[str] = Query(..., min_length=2, description="Имя."),
                      phone: Optional[int] = Query(..., description="Номер телефона.")):
    users_dct = my_mini_db.load_data()
    my_message = my_mini_db.add_user(users_dct, username, firstname, phone)
    my_mini_db.save_data(users_dct)
    return {"message": my_message}


@app.delete("/user/{user-name}", tags=["user"])
async def delete_user(username: Optional[str] = Query(...,
                                                      min_length=2,
                                                      description="Никнейм пользователя которого требуется удалить.")):
    users_dct = my_mini_db.load_data()
    my_message = my_mini_db.delete_user(users_dct, username)
    my_mini_db.save_data(users_dct)
    return {"message": my_message}


@app.delete("/user", tags=["users"])
async def delete_all_users():
    my_message = my_mini_db.delete_all_user()
    return {"message": my_message}


@app.get("/user/{user-name}", tags=["user"])
async def search_by_name(username: Optional[str] = Query(...,
                                                         min_length=2,
                                                         description="Никнейм интересующего пользователя.")):
    users_dct = my_mini_db.load_data()
    return {"message": users_dct.get(username, 'Это имя не найдено.')}


@app.put("/user/{user-name}", tags=["user"])
async def change_user(username: Optional[str] = Query(..., min_length=2, description="Никнейм."),
                      new_username: Optional[str] = Query(..., min_length=2, description="Новый никнейм."),
                      new_firstname: Optional[str] = Query(..., min_length=2, description="Новое имя."),
                      new_phone: Optional[int] = Query(..., description="Новый номер телефона.")):
    users_dct = my_mini_db.load_data()
    if users_dct.get(username):
        my_mini_db.delete_user(users_dct, username)
        my_mini_db.add_user(users_dct, new_username, new_firstname, new_phone)
        my_mini_db.save_data(users_dct)
        return {"message": "Данные успешно изменены."}
    return {"message": "Такого пользователя не существует."}


@app.get("/user/{create-with-list}", tags=["users"])
async def show_all_users():
    users_dct = my_mini_db.load_data()
    return users_dct


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8004)
