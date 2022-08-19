from rest_framework.views import APIView
from rest_framework.response import Response
from base.models import Gallery
from ..helpers import get_drive_service

class GalleryImages(APIView):
    def get(self, request, id):
        gallery = Gallery.objects.filter(id=id).prefetch_related('storage_backend').first()
        # The default gallery has not been created yet
        if gallery is None:
            return Response(data=[])
        
        files = self.fetch(gallery)
        
        return Response(data=files)
    
    def fetch(self, gallery):
        """
        Retrieve image files from this gallery’s folder 
        """
        
        service = get_drive_service(
            gallery.storage_backend.meta['access_token'],
            gallery.storage_backend.meta['refresh_token'],
        )
        
        query = f"parents = '{gallery.folder_id}'"
        fields = 'files(id, name, imageMediaMetadata, thumbnailLink)'

        res = service.files().list(q=query, fields=fields).execute()
        
        files = res.get('files', [])
        
        return files