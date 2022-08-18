from django.urls import path
from . import views

urlpatterns = [
    path('storage-backends/connect', views.ConnectStorageBackend.as_view()),
    path('auth/user', views.CurrentUser.as_view())
]