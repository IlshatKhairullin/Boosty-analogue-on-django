import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


def test_status(api_client):
    response = api_client.get(reverse("status"))
    assert response.status_code == status.HTTP_200_OK


# def test_posts(api_client):
#     response = api_client.get(reverse("posts"))
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.json()) > 0
