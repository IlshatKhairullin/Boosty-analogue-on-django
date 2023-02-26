from django.contrib import admin

from web.models import Comment


class PostCommentInline(admin.TabularInline):
    model = Comment
    readonly_fields = ("author", "parent")


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "post",
        "author",
        "body",
    )

    # запрещаем удаление коммента через админку, но если коммент твой - то ок
    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return False
        return request.user == obj.author

    # изменение
    def has_change_permission(self, request, obj=None):
        return False

    # добавление
    def has_add_permission(self, request):
        return False
