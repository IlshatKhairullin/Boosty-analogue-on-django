from django.urls import path

from api.views import status_view, posts_view, post_view, UserAPIList, UserAPIDetailView

urlpatterns = [
    path("", status_view, name="status"),
    path("posts/", posts_view, name="posts"),
    path("posts/<int:pk>/", post_view, name="post"),
    path("users/", UserAPIList.as_view(), name="users"),
    path("users/detail/<int:pk>/", UserAPIDetailView.as_view(), name="user"),
]
