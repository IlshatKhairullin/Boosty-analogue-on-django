import factory

from web.models import Post, User, Comment
from web.enums import Status


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")
    username = factory.Faker("user_name")

    class Meta:
        model = User


class PostFactory(factory.django.DjangoModelFactory):
    author = factory.SubFactory(UserFactory)
    title = factory.Faker("word")
    body = factory.Faker("text")
    status = Status.published

    class Meta:
        model = Post


class CommentFactory(factory.django.DjangoModelFactory):
    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    body = factory.Faker("text")

    class Meta:
        model = Comment
