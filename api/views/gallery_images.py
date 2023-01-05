from rest_framework.views import APIView
from rest_framework.response import Response
from base.models.gallery import Gallery
from api.helpers import fetchGalleryImages

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
            
        files = fetchGalleryImages(gallery)
        
        return Response(data=files)
