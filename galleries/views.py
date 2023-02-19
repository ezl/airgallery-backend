from django.utils import timezone
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from galleries.filters import ImageFilter
from galleries.models import Gallery, Image
from galleries.serializers import GallerySerializer, ImageSerializer, GalleryCreateSerializer, GalleryUpdateSerializer


class GalleryViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GallerySerializer
        elif self.request.method == 'POST':
            return GalleryCreateSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return GalleryUpdateSerializer

    queryset = Gallery.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug' #TODO: rename to uuid, this field isn't actually a slug

    def create(self, request, *args, **kwargs):
        ## TODO - Eric
        #WIP: made with Robert. Not in use.
        serializer = GalleryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Gallery.objects.create(
            name=serializer.validated_data['name'],
            slug=serializer.validated_data['name'].lower(),
            user=request.user
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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

        # We need to get thumbnail urls.
        # to do that, we need to query on the specific folder, which
        # means we need to go up to the gallery (otherwise it'll
        # search the user's entire google drive)

        # alternatively need a way to do a bulk search for a list of
        # file ids, but i couldn't find documentation for that

        gallery_id = request.query_params.get('gallery')
        gallery = Gallery.objects.get(id=gallery_id)

        # returns google's representation, which includes a thumbnail link
        google_drive_images = gallery.fetch_image_thumbnails()

        # TODO: OK this is the big sin. We need to get the thumbnail links into
        # the response. Doing this VERY inefficiently and won't make sense.
        # SHOULD be using a batch operation to get these from the ids then using a callback
        # but instead doing this stupid thing.
        # https://github.com/googleapis/google-api-python-client/blob/main/docs/batch.md

        for image_data in serialized_images:
            file_id = image_data['file_id']
            google_object = next((item for item in google_drive_images if item.get('id') == file_id), None)
            # get the google object that corresponds to the same object from the Image table (matched on google file id)
            thumbnail_link = google_object['thumbnailLink']
            image_data['thumbnail_link'] = thumbnail_link

        return Response(serializer.data)

