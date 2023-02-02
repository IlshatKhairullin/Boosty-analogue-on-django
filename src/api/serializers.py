from rest_framework import serializers
from django.utils.text import slugify

from web.models import Post, User, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "body", "author_id", "created_date")


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post_comments = CommentSerializer(many=True, read_only=True)
    body = serializers.CharField(write_only=True)

    # проверяет все атрибуты сериализатора и выкидывает исключение если что то не так
    def validate(self, attrs):
        attrs["author"] = User.objects.last()  # attrs['author'] = self.context['request'].user.id
        attrs["slug"] = slugify(attrs["title"])
        return attrs

    class Meta:
        model = Post
        fields = ("id", "title", "body", "author", "post_comments", "status")
