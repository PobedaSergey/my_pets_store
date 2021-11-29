from fastapi.testclient import TestClient

import main


# TODO написать тестовую функцию?


# def test_show_user():
#     with TestClient(main.app) as client:
#         response = client.get("/user/1")
#         assert response.status_code == 200
#
#
# test_show_user()


def test_create_user():
    with TestClient(main.app) as client:
        response = client.post("/user/")
        assert response.status_code == 200


test_create_user()


import logging


