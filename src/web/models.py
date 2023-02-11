from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import QuerySet, Count
from django.urls import reverse
from taggit.managers import TaggableManager

from web.enums import Status


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    email = models.EmailField("Email", unique=True)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="user_avatars")
    profile_background = models.ImageField(null=True, blank=True, upload_to="user_backgrounds")
    vk_url = models.CharField(max_length=255, null=True, blank=True)
    github_url = models.CharField(max_length=255, null=True, blank=True)
    is_private = models.BooleanField(default=False)
    send_comment_on_post_notification = models.BooleanField(default=False)


class PostQuerySet(QuerySet):
    def optimize_for_post_info(self):
        return (
            self.select_related("author")
            .prefetch_related("post_comments")
            .annotate(total_views=Count("views", distinct=True))
            .annotate(total_likes=Count("likes", distinct=True))
            .annotate(total_comments=Count("post_comments", distinct=True))
        )


class Post(BaseModel):
    objects = PostQuerySet.as_manager()

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.draft)
    tags = TaggableManager(blank=True)
    likes = models.ManyToManyField(User, related_name="post_like", blank=True)
    views = models.ManyToManyField(User, related_name="post_views", blank=True)

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.slug, self.id])

    def get_edit_absolute_url(self):
        return reverse("post_edit_detail", args=[self.slug, self.id])

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title


class Comment(BaseModel):
    post = models.ForeignKey(Post, related_name="post_comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="commenter")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    body = models.TextField(verbose_name="comment_text")
    is_active = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name="post_comment_like")

    @property
    def children(self):  # replies to comment
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

    class Meta:
        ordering = ("-created_date",)
