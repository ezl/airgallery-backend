from rest_framework.views import APIView
from rest_framework.response import Response
from galleries.models import Gallery

class GalleryImages(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, id):
        gallery = Gallery.objects.filter(
            id=id,
            published_at__isnull=False
        ).prefetch_related('storage_backend').first()

        if gallery is None:
            return Response(data=[])

        files = gallery.fetch_images()

        return Response(data=files)
