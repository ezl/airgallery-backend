from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from galleries.views import GalleryViewSet, ImageViewSet
from user_profiles.views import UserViewSet
from storage_backends.views import StorageBackendViewSet


router = routers.DefaultRouter()
router.register(r'galleries', GalleryViewSet)
router.register(r'images', ImageViewSet)
router.register(r'users', UserViewSet)
router.register(r'storage_backends', StorageBackendViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('/', include("base.urls")),
    path('api/', include("api.urls")),
    path('admin/', admin.site.urls),
]
