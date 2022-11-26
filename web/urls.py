from django.urls import path, include
from web import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('home/', views.PostListView.as_view(), name='post_list'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.login, name='login'),
    path('home/<slug:slug>/<int:id>', views.DetailPostView.as_view(), name='post_detail'),
    path('post_like/<slug:post_slug>/<int:post_id>', views.LikePostView, name='post_like'),
    path('comment_like/<slug:post_slug>/<int:post_id>/<int:comment_id>', views.LikeCommentView, name='comment_like'),
    path('home/<slug:tag_slug>/', views.TagIndexView.as_view(), name='posts_by_tag'),
    path('home/<slug:slug>/<int:post_id>/comment/<int:id>/delete', views.DeleteCommentView.as_view(), name='comment_delete'),
    path('home/<slug:slug>/<int:post_id>/comment/<int:id>/edit', views.UpdateCommentView.as_view(), name='comment_edit'),
    path('profile/stats', views.ProfileView.as_view(), name='profile_post_stats'),
    path('profile/edit/<int:id>', views.ProfileUserEditView.as_view(), name='user_profile_edit'),
    path('profile/settings/<int:id>', views.ProfileSettings.as_view(), name='user_profile_settings'),
    path('profile/my_posts', views.ProfileUserPostsView.as_view(), name='profile_user_posts'),
    path('profile/my_posts/<slug:slug>/<int:id>', views.DetailPostEditView.as_view(), name='post_edit_detail'),
    path('profile/my_posts/post-add/', views.PostCreateFormView.as_view(), name='post_create'),
    path('profile/my_posts/<str:slug>/<int:id>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('profile/my_posts/<str:slug>/<int:id>/edit', views.PostUpdateView.as_view(), name='post_edit')
]
