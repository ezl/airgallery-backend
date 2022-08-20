from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import GallerySerializer
from django.utils import timezone

class ToggleGalleryPublication(APIView):
    def patch(self, request, id):
        gallery = request.user.gallery_set.filter(id=id).first()
        
        if gallery is None:
            return Response('', status=status.HTTP_404_NOT_FOUND)
        
        if gallery.published_at is None:
            gallery.published_at = timezone.now()
        else:
            gallery.published_at = None
            
        gallery.save()
        
        gallery_serializer = GallerySerializer(instance=gallery)
    
        return Response(gallery_serializer.data)
        