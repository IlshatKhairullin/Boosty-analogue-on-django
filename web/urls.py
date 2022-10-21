from django.urls import path, include
from web import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('home/', views.PostListView.as_view(), name='post_list'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.login, name='login'),
    path('home/<slug:slug>/<int:id>', views.DetailPostView.as_view(), name='post_detail'),
    path('home/<slug:tag_slug>/', views.TagIndexView.as_view(), name='posts_by_tag'),
    path('home/<slug:slug>/<int:post_id>/comment/<int:id>/delete', views.DeleteCommentView.as_view(), name='comment_delete'),
    path('home/<slug:slug>/<int:post_id>/comment/<int:id>/edit', views.UpdateCommentView.as_view(), name='comment_edit'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<slug:slug>/<int:id>', views.DetailPostEditView.as_view(), name='post_edit_detail'),
    path('profile/post-add/', views.PostCreateFormView.as_view(), name='post_create'),
    path('profile/<str:slug>/<int:id>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('profile/<str:slug>/<int:id>/edit', views.PostUpdateView.as_view(), name='post_edit')
]
