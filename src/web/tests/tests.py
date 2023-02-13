from http import HTTPStatus
from random import randint
from django.test import TestCase
from django.urls import reverse
from requests import Response

from web.tests.factories import PostFactory


class UnauthorizedTestCase(TestCase):
    def test_unauthorized(self):
        response = self.client.get(reverse("post_list"))
        registration_link = reverse("register")
        self.assertContains(response, registration_link)


class MainPageTestCase(TestCase):
    def setUp(self) -> None:  # запускается перед каждым тестом
        self.post = PostFactory()
        self.client.force_login(self.post.author)

    def _check_response(self, page: str, equal: bool = True, query_params: dict = None) -> Response:
        response = self.client.get(reverse(page), data=query_params)
        if equal:
            self.assertEqual(response.status_code, HTTPStatus.OK)
        else:
            self.assertNotEqual(response.status_code, HTTPStatus.OK)
        return response

    def test_post_list(self):
        response = self._check_response(page="post_list")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.post.title)

    def test_post_list_with_search(self):
        response = self._check_response(page="post_list", query_params={"search": self.post.title})
        self.assertContains(response, self.post.title)

    def test_post_list_with_search_empty(self):
        response = self._check_response(
            page="post_list", query_params={"search": randint(100, 200)}
        )  # factory.Faker(text) вернет только строку
        self.assertNotContains(response, self.post.title)

    def test_post_like_on_main_page(self):
        response = self.client.post(
            reverse("post_like", args=(self.post.slug, self.post.id)),
            {"post_like_main_page": self.post.id},
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
