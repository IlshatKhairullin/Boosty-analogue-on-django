from django.urls import path

from api.views import status_view, posts_view, post_view

urlpatterns = [
    path("", status_view, name="status"),
    path("posts/", posts_view, name="posts"),
    path("posts/<int:id>/", post_view, name="post"),
]
