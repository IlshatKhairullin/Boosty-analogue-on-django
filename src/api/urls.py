from django.urls import path, include
from rest_framework import routers

from api.views import status_view, posts_view, post_view, UserViewSet, NoteViewSet

# роутеры помогают не прописывать пути, предоставляют совсем общие шаблоны - users/ лист юзеров,
# user/4/ - конкретный юзер
router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"notes", NoteViewSet, basename="notes")

# если же роутеры не подходят, то url с помощью viewset'ов можно написать так:
# path('api/v1/userlist/', UserViewSet.as_view({'get': 'list'})), название в документации - viewset actions
# path('api/v1/user/<int:pk>/', UserViewSet.as_view({'put': 'update'}))
# viewset один, а пути разные в зависимости от http-запроса

urlpatterns = [
    path("", status_view, name="status"),
    path("posts/", posts_view, name="posts"),
    path("posts/<int:pk>/", post_view, name="post"),
] + router.urls
