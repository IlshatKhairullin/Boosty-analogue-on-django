from web.admin.post import AuthorEmailDomainFilter
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


class EmailDomainFilter(AuthorEmailDomainFilter):
    title = "Домен пользователя"
    parameter_name = "user_email_domain"

    # переопределили родительские атрибуты и метод queryset
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(email__endswith=f"@{self.value()}")
        return queryset


class MyUserAdmin(UserAdmin):
    list_display = ("id", "email", "username", "is_staff")
    ordering = ("-date_joined",)
    list_filter = ("send_comment_on_post_notification", "date_joined", "last_login", "is_staff", EmailDomainFilter)
    # поля внутри редактирования
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": ("is_staff",),
            },
        ),
        (_("Dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
