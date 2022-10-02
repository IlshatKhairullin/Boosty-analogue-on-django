from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

User = get_user_model()


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    title = models.CharField(max_length=500)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class AuthorInfo(models.Model):
    description = models.CharField(max_length=500)
    goals = models.CharField(max_length=500)


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
