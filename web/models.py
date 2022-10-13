from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from web.enums import Status


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    email = models.EmailField('Email', unique=True)


class Post(BaseModel):  # добавить атрибуты, чтобы были похожи на объявления (цену, еще что то)
    # + добавить категории к постам
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=0)
    publish = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.draft)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug, self.id])

    def get_edit_absolute_url(self):
        return reverse('post_edit_detail', args=[self.slug, self.id])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


# class Tag(BaseModel):
#     title = models.CharField(max_length=200)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     parent_tag = models.ForeignKey(
#         "self",
#         on_delete=models.SET_NULL,
#         null=True
#     )

class AuthorInfo(models.Model):
    description = models.CharField(max_length=500)
    goals = models.CharField(max_length=500)
    img = models.ImageField(null=True)


# class Subscriber(models.Model):
#     user = models.ForeignKey(User, related_name='subscriber',
#                              on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Comment(BaseModel):
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    body = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
