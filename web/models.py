from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager

from web.enums import Status


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    email = models.EmailField('Email', unique=True)


class Post(BaseModel):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.draft)
    tags = TaggableManager()
    likes = models.ManyToManyField(User, related_name='blog_post_from_like')

    def number_of_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug, self.id])

    def get_edit_absolute_url(self):
        return reverse('post_edit_detail', args=[self.slug, self.id])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class AuthorInfo(models.Model):
    description = models.CharField(max_length=500)
    goals = models.CharField(max_length=500)
    img = models.ImageField(null=True)


# class Subscriber(models.Model):
#     user = models.ForeignKey(User, related_name='subscriber',
#                              on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()


class IsActiveFilterComments(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Comment(BaseModel):
    post = models.ForeignKey(Post, related_name='comments_posts', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='commenter')
    body = models.TextField(verbose_name='comment_text')
    is_active = models.BooleanField(default=True)
    objects = IsActiveFilterComments()
    likes = models.ManyToManyField(User, related_name='post_comment_like')

    def number_of_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
