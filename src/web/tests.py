from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from requests import Response

from web.models import User, Post
from web.enums import Status


class MainPageTestCase(TestCase):
    def _check_response(self, page: str, equal: bool = True, query_params: dict = None) -> Response:
        response = self.client.get(reverse(page), data=query_params)
        if equal:
            self.assertEqual(response.status_code, HTTPStatus.OK)
        else:
            self.assertNotEqual(response.status_code, HTTPStatus.OK)
        return response

    def test_post_list(self):
        user = User.objects.create(email="test@yandex.ru")
        post = Post.objects.create(
            title="test post", slug=slugify("test post"), author=user, body="test", status=Status.published
        )
        self.client.force_login(user)
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, post.title)
