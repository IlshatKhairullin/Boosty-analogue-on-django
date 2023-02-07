from django.contrib import admin
from django.contrib import messages
from web.models import Post, User
from web.admin.comment import PostCommentInline

from web.db_utils import SplitPartFunc


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


# кастомный фильтр по домену автора поста
class AuthorEmailDomainFilter(admin.SimpleListFilter):
    title = "Домен автора поста"
    parameter_name = "author_email_domain"

    def has_output(self):
        return True

    # annotate - добавляет новое поле в queryset, values_list - из всего множества полей выбирает только одно указанное,
    # flat=True - список значений вместо одиночных кортежей
    def lookups(self, request, model_admin):
        email_domains = (
            User.objects.all()
            .annotate(email_domain=SplitPartFunc("email", "@", 2))
            .distinct()
            .values_list("email_domain", flat=True)
        )
        return (
            (d, d) for d in email_domains
        )  # 1 зн-е пойдет в адресную строку(параметр фильтрации), 2 зн-е - то, как будет отображаться у юзера

    def queryset(self, request, queryset):
        if self.value():  # берем значение из параметра запроса(каждый фильтр - новый класс, со своим value в url)
            return queryset.filter(author__email__endswith=f"@{self.value()}")
        return queryset


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "body",
        "author",
        "get_author_email",
        "publish",
        "status",
    )  # то, что выводится на экран
    list_display_links = ("id", "title")  # ссылки на объекты(теперь не только по id можно перейти)
    list_filter = (
        "status",
        "created_date",
        "publish",
        "author",
        "tags",
        AuthorEmailDomainFilter,
    )  # фильтрация справа sidebar
    search_fields = ("title", "body")  # идет поиск по данным полям
    # prepopulated_fields = {"slug": ("title",)}  # предзаполнение полей
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("-publish",)  # порядок по умолчанию
    readonly_fields = ("likes", "views", "get_text_count")
    exclude = ("slug",)  # убрать поле из видимости совсем
    actions = (set_title_to_uppercase,)  # тут объявляем действия
    inlines = (PostCommentInline,)  # inlines работают только для FK, выводит список комментов на посте

    # какие то свои поля с логикой можно описать так
    @admin.display(description="Text count")  # поменяли название у поля
    def get_text_count(self, instance):
        return len(instance.body)

    @admin.display(description="Email")
    def get_author_email(self, obj):
        return obj.author.email
