from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CurrentUserGalleryImages(APIView):
    def get(self, request):
        #raise Exception
        gallery = request.user.gallery_set.prefetch_related('storage_backend').first()

        if gallery is None:
            return Response(data=[])

        files = gallery.fetch_image_thumbnails()
        return Response(data=files)
