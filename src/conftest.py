import pytest

from web.tests.factories import PostFactory, UserFactory


@pytest.fixture(autouse=True)
def init_db(db):  # поднимает локальную базу при каждом запуске теста, не мешает юниттестам
    pass


@pytest.fixture()
def post():
    return PostFactory()


@pytest.fixture()
def user():
    return UserFactory()
