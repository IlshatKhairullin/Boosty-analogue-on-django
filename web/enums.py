from django.db import models


class Status(models.TextChoices):
    draft = 'Draft', 'Черновик'
    published = 'Published', 'Опубликовано'
