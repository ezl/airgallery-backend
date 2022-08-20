from django.urls import path
from . import views

urlpatterns = [
    path('storage-backends/connect', views.ConnectStorageBackend.as_view()),
    path('upload/drive', views.DriveUploadImage.as_view()),
    path('galleries/by-slug/<str:slug>', views.SingleGallery.as_view()),
    path('galleries/<int:id>/toggle-publication', views.ToggleGalleryPublication.as_view()),
    path('galleries/<int:id>/images', views.GalleryImages.as_view()),
    path('auth/user', views.CurrentUser.as_view()),
    path('auth/user/gallery', views.CurrentUserGallery.as_view()),
    path('auth/user/gallery/images', views.CurrentUserGalleryImages.as_view())
]