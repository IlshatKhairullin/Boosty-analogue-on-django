from django.urls import path

from api.views import status_view, posts_view, post_view, UserAPIView

urlpatterns = [
    path("", status_view, name="status"),
    path("posts/", posts_view, name="posts"),
    path("posts/<int:pk>/", post_view, name="post"),
    path("users/", UserAPIView.as_view(), name="users"),
    path("users/<int:pk>/", UserAPIView.as_view(), name="user"),
]
