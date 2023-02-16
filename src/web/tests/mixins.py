from requests import Response
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from web.tests.factories import PostFactory


class PostTestMixin(TestCase):
    def setUp(self) -> None:  # запускается перед каждым тестом
        self.post = PostFactory()
        self.client.force_login(self.post.author)

    def _check_response(self, page: str, equal: bool = True, query_params: dict = None, **kwargs) -> Response:
        response = self.client.get(reverse(page, kwargs=kwargs), data=query_params)
        if equal:
            self.assertEqual(response.status_code, HTTPStatus.OK)
        else:
            self.assertNotEqual(response.status_code, HTTPStatus.OK)
        return response
