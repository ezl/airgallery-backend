from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import GallerySerializer

class CurrentUserGallery(APIView):
    def get(self, request):
        raise Exception
        gallery = request.user.gallery_set.first()
        
        if gallery is None:
            return Response('', status=status.HTTP_404_NOT_FOUND)
        
        gallery_serializer = GallerySerializer(instance=gallery)
    
        return Response(gallery_serializer.data)
        
