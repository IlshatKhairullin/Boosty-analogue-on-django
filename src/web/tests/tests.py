from http import HTTPStatus
from random import randint
from django.test import TestCase
from django.urls import reverse

from web.tests.mixins import PostTestMixin


class UnauthorizedTestCase(TestCase):  # unittest's below
    def test_unauthorized(self):
        response = self.client.get(reverse("post_list"))
        registration_link = reverse("register")
        self.assertContains(response, registration_link)


class MainPageTestCase(PostTestMixin):
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

    def test_post_like_main_page(self):
        response = self.client.post(
            reverse("post_like", args=(self.post.slug, self.post.id)),
            {"post_like_main_page": self.post.id},
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)


class PostDetailPageTestCase(PostTestMixin):
    def test_post_detail(self):
        response = self._check_response(page="post_detail", slug=self.post.slug, id=self.post.id)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_send_comment_post_detail(self):
        response = self.client.post(
            reverse("post_detail", args=(self.post.slug, self.post.id)), data={"body": "123"}, follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_comment_like_post_detail(self):
        response = self.client.post(
            reverse("comment_like", args=(self.post.slug, self.post.id, self.comment.id)),
            {"comment_like": self.comment.id},
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
