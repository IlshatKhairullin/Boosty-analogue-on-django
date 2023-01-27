from django.urls import path, include
from django.contrib.auth.decorators import login_required

from web import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("home/", views.PostListView.as_view(), name="post_list"),
    path("login/", views.login_view, name="login"),
    path("register/", views.Register.as_view(), name="register"),
    path("home/<slug:slug>/<int:id>", views.DetailPostView.as_view(), name="post_detail"),
    path("post_like/<slug:post_slug>/<int:post_id>", views.LikePostView, name="post_like"),
    path("comment_like/<slug:post_slug>/<int:post_id>/<int:comment_id>", views.LikeCommentView, name="comment_like"),
    path("home/<slug:tag_slug>/", views.TagIndexView.as_view(), name="posts_by_tag"),
    path(
        "home/<slug:slug>/<int:post_id>/comment/<int:id>/delete",
        login_required(views.DeleteCommentView.as_view()),
        name="comment_delete",
    ),
    path(
        "home/<slug:slug>/<int:post_id>/comment/<int:id>/edit",
        login_required(views.UpdateCommentView.as_view()),
        name="comment_edit",
    ),
    path("author/<int:id>", views.AuthorProfile.as_view(), name="author_profile"),
    path("profile/stats", login_required(views.ProfileView.as_view()), name="profile_post_stats"),
    path("profile/", login_required(views.LikedPostsListView.as_view()), name="profile_liked_posts"),
    path("profile/edit/<int:id>", login_required(views.ProfileUserEditView.as_view()), name="user_profile_edit"),
    path("profile/settings/<int:id>", login_required(views.ProfileSettings.as_view()), name="user_profile_settings"),
    path("profile/my_posts", login_required(views.ProfileUserPostsView.as_view()), name="profile_user_posts"),
    path(
        "profile/my_posts/<slug:slug>/<int:id>",
        login_required(views.DetailPostEditView.as_view()),
        name="post_edit_detail",
    ),
    path("profile/my_posts/post-add/", login_required(views.PostCreateView.as_view()), name="post_create"),
    path(
        "profile/my_posts/<str:slug>/<int:id>/delete",
        login_required(views.PostDeleteView.as_view()),
        name="post_delete",
    ),
    path("profile/my_posts/<str:slug>/<int:id>/edit", login_required(views.PostUpdateView.as_view()), name="post_edit"),
]
