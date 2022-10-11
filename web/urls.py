from django.urls import path, include
from web import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('home/', views.PostListView.as_view(), name='post_list'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.login, name='login'),
    path('home/<slug:slug>/<int:id>', views.DetailPostView.as_view(), name='post_detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<str:title>/<int:id>', views.DetailPostEditView.as_view(), name='post_edit_detail'),
    path('profile/post-add/', views.PostCreateFormView.as_view(), name='post_create'),
    path('profile/<str:title>/<int:id>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('profile/<str:title>/<int:id>/edit', views.PostUpdateView.as_view(), name='post_edit')
]
