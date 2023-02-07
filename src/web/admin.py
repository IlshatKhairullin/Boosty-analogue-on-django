from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages

from .models import Post, User, Comment

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


# так можно создавать свои действия в админке(на подобии удаления)
@admin.display(description="Привести названия к верхнему регистру")
def set_title_to_uppercase(modeladmin, request, queryset):
    objects = []

    for item in queryset:
        item.title = item.title.upper()
        objects.append(item)
    Post.objects.bulk_update(
        objects, ["title"]
    )  # не через save, тк будет куча sql-запросов к базе(к каждому объекту списка)

    messages.add_message(request, messages.SUCCESS, f"Обновлено {len(objects)} объектов")  # сообщение при успехе


class PostCommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "body", "author", "publish", "status")  # то, что выводится на экран
    list_display_links = ("id", "title")  # ссылки на объекты(теперь не только по id можно перейти)
    list_filter = ("status", "created_date", "publish", "author")  # фильтрация справа sidebar
    search_fields = ("title", "body")  # идет поиск по данным полям
    # prepopulated_fields = {"slug": ("title",)}  # предзаполнение полей
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("-publish",)  # порядок по умолчанию
    readonly_fields = ("author", "likes", "views", "get_text_count")
    exclude = ("slug",)  # убрать поле из видимости совсем
    actions = (set_title_to_uppercase,)  # тут объявляем действия
    inlines = (PostCommentInline,)  # inlines работают только для FK, выводит список комментов на посте

    # какие то свои поля с логикой можно описать так
    @admin.display(description="Text count")  # поменяли название у поля
    def get_text_count(self, instance):
        return len(instance.body)


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


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
