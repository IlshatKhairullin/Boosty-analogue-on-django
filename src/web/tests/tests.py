from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from requests import Response

from web.tests.factories import PostFactory


class MainPageTestCase(TestCase):
    def _check_response(self, page: str, equal: bool = True, query_params: dict = None) -> Response:
        response = self.client.get(reverse(page), data=query_params)
        if equal:
            self.assertEqual(response.status_code, HTTPStatus.OK)
        else:
            self.assertNotEqual(response.status_code, HTTPStatus.OK)
        return response

    def test_post_list(self):
        post = PostFactory()
        self.client.force_login(post.author)
        response = self._check_response(page="post_list")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, post.title)
