from django.urls import path
from . import views

urlpatterns = [
    path('storage-backends/connect', views.ConnectStorageBackend.as_view()),
    path('upload/drive', views.DriveUploadImage.as_view()),
    path('gallery/<int:id>/images', views.GalleryImages.as_view()),
    path('auth/user', views.CurrentUser.as_view())
]