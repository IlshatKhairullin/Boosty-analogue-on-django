from rest_framework import serializers
from django.utils.text import slugify

from web.models import Post, User, Comment


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    send_comment_on_post_notification = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "send_comment_on_post_notification")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "body", "author_id", "created_date")


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post_comments = CommentSerializer(many=True, read_only=True)
    body = serializers.CharField()

    # проверяет все атрибуты сериализатора и выкидывает исключение если что то не так
    def validate(self, attrs):
        attrs["author"] = User.objects.last()  # attrs['author'] = self.context['request'].user.id
        attrs["slug"] = slugify(attrs["title"])
        return attrs

    class Meta:
        model = Post
        fields = ("id", "title", "body", "status", "author", "post_comments")
