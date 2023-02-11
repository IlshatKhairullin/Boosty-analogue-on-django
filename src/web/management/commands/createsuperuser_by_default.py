from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from web.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        password = "123"
        user = User(is_staff=True, is_superuser=True, username=123, password=make_password(password))
        user.save()
        print(f"superuser created, username - {user.username}, password - {user.password}")
