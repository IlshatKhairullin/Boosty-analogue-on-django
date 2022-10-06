from django.urls import path, re_path, include
from web import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('home/', views.PostListView.as_view(), name='post_list'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.login, name='login'),
    re_path(r'^(?P<post>[-\w]+)/(?P<id>\d+)$', views.DetailPostView.as_view(),
            name='post_detail')
]
