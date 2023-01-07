from rest_framework import viewsets
from rest_framework import permissions

from galleries.models import Gallery
from api.serializers.gallery_serializer import GallerySerializer


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [permissions.AllowAny]
