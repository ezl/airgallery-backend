from rest_framework import viewsets
from rest_framework import permissions

from galleries.models import Gallery, Image
from galleries.serializers import GallerySerializer, ImageSerializer


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug' #TODO: rename to uuid, this field isn't actually a slug

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.AllowAny]

