from rest_framework.views import APIView
from rest_framework.response import Response
from galleries.models import Gallery

class GalleryImages(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, id):
        # raise Exception("TODO: Eric remove this. we should be using the DRF endpoint in the galleries model")
        gallery = Gallery.objects.filter(
            id=id,
            published_at__isnull=False
        ).prefetch_related('storage_backend').first()

        if gallery is None:
            return Response(data=[])

        files = gallery.fetch_image_thumbnails()

        return Response(data=files)
