from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from galleries.models import Gallery
from api.serializers import GallerySerializer

class SingleGallery(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, slug):
        # raise Exception("TODO: note to Eric to remove this. This has been replaced by a ModelViewSet in the Gallery app")
        gallery = Gallery.objects.filter(
            slug=slug,
            published_at__isnull=False
        ).prefetch_related('user').first()

        if gallery is None:
            return Response('', status=status.HTTP_404_NOT_FOUND)

        gallery_serializer = GallerySerializer(instance=gallery)

        return Response(gallery_serializer.data)

