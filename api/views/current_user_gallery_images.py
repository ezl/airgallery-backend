from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..helpers import fetchGalleryImages

class CurrentUserGalleryImages(APIView):
    def get(self, request):
        gallery = request.user.gallery_set.prefetch_related('storage_backend').first()
        
        if gallery is None:
            return Response(data=[])
            
        files = fetchGalleryImages(gallery)
        
        return Response(data=files)