from django.urls import path

from api.views import status_view

urlpatterns = [
    path("", status_view),
]
