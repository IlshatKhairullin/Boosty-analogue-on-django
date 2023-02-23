import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from web.enums import Status


@pytest.fixture
def api_client():
    return APIClient()


def test_status(api_client):  # pytest's below
    response = api_client.get(reverse("status"))
    assert response.status_code == status.HTTP_200_OK


def test_posts(api_client, post):  # post - обращение к фикстуре в conftest.py
    response = api_client.get(reverse("posts"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0


def test_post(api_client, post):
    response = api_client.get(reverse("post", args=(post.id,)))
    assert response.status_code == status.HTTP_200_OK
    assert post.id == response.json()["id"]  # проверка на соответствие id созданного и того, что пришло


def test_post_create(api_client, user):
    response = api_client.post(
        reverse("posts"),
        data={"author": user, "title": "post title", "body": "lorem ipsum", "status": Status.published},
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_post_full_update(api_client, post, user):
    response = api_client.put(
        reverse("post", args=(post.id,)),
        data={"author": user, "title": "post title", "body": "lorem ipsum", "status": Status.published},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    post.refresh_from_db()  # подтягиваем изменения из бд
    assert post.title == "post title"


def test_users(api_client, user):
    response = api_client.get(reverse("users-list"))
    assert response.status_code == status.HTTP_200_OK


def test_user(api_client, user):
    response = api_client.get(reverse("users-detail", args=(user.id,)))
    assert response.status_code == status.HTTP_200_OK
    assert user.id == response.json()["id"]


def test_user_create(api_client):
    response = api_client.post(reverse("users-list"), data={"username": "Test", "email": "Test@yandex.ru"})
    response_json = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert response_json["username"] == "Test" and response_json["email"] == "Test@yandex.ru"


def test_user_update(api_client, user):  # видимо part update doesn't require refresh, в отличии от post запроса
    response = api_client.patch(reverse("users-detail", args=(user.id,)), data={"username": "part_update_username"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "part_update_username"


def test_user_delete(api_client, user):
    response = api_client.delete(reverse("users-detail", args=(user.id,)))
    assert response.status_code == status.HTTP_204_NO_CONTENT
