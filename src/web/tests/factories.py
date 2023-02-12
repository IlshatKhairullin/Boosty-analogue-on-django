import factory

from web.models import Post, User
from web.enums import Status


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")

    class Meta:
        model = User


class PostFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("word")
    body = factory.Faker("text")
    author = factory.SubFactory(UserFactory)
    status = Status.published

    class Meta:
        model = Post
