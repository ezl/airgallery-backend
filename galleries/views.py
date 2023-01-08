from django.utils import timezone
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from galleries.models import Gallery, Image
from galleries.serializers import GallerySerializer, ImageSerializer


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug' #TODO: rename to uuid, this field isn't actually a slug

    @action(detail=True, methods=['patch'])
    def publish(self, request, slug=None):
        gallery = self.get_object()
        gallery.published_at = timezone.now()
        gallery.save()
        serializer = self.get_serializer(gallery)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def unpublish(self, request, slug=None):
        gallery = self.get_object()
        gallery.published_at = None #TODO: this should be turned into 2 fields. "published" boolean and "last_published" = timestamp or None
        gallery.save()
        serializer = self.get_serializer(gallery)
        return Response(serializer.data)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.AllowAny]

