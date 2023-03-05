from django.urls import path, re_path, include
from rest_framework import routers
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from api.views import status_view, posts_view, post_view, UserViewSet, NoteViewSet

# роутеры помогают не прописывать пути, предоставляют совсем общие шаблоны - users/ лист юзеров,
# user/4/ - конкретный юзер
router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="users")

# также вместо SimpleRouter можно объявить DefaultRouter, отличие только в том, что при запросе на главный урл
# (сейчас он определен как status view), будет возвращаться ссылка на урл со списком элементов (post-list)
default_router = routers.DefaultRouter()
default_router.register(r"notes", NoteViewSet, basename="notes")

# если же роутеры не подходят, то url с помощью viewset'ов можно написать так:
# path('api/v1/userlist/', UserViewSet.as_view({'get': 'list'})), название в документации - viewset actions
# path('api/v1/user/<int:pk>/', UserViewSet.as_view({'put': 'update'}))
# viewset один, а пути разные в зависимости от http-запроса
# также можно легко определять свои кастомные роутеры(при необходимости)

schema_view = get_schema_view(
    openapi.Info(
        title="Posts API",
        default_version="v1",
        description="django test project",
        contact=openapi.Contact(email="developer@posts.com"),
    ),
    public=True,
    permission_classes=[],
)

urlpatterns = (
    [
        path("", status_view, name="status"),
        path("drf-auth/", include("rest_framework.urls")),
        path("posts/", posts_view, name="posts"),
        path("posts/<int:pk>/", post_view, name="post"),
        re_path("^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
        path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]
    + router.urls
    + default_router.urls
)
