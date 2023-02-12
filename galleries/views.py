from django.utils import timezone
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from galleries.filters import ImageFilter
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
    filterset_class = ImageFilter


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        serialized_images = serializer.data
        
        for image_data in serialized_images:
            file_id = image_data['file_id']

            thumbnail_url = google_service.fetch_file_metadata(file_id)
            image_data['thumbnail_url'] = thumbnail_url
            
        return Response(serializer.data)

