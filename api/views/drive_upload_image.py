from rest_framework.views import APIView
from rest_framework.response import Response
from base.models import User, StorageBackend, Gallery, Image
from ..helpers import get_drive_service, get_mime_type
import io

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

class DriveUploadImage(APIView):
    def put(self, request):
        gallery = self.get_or_create_gallery(request.user)
        file = request.FILES['image'] 
        
        new_file = self.upload(gallery, file)
        
        self.create_image(gallery, new_file)
        
        return Response(data=new_file)
        
    def get_or_create_gallery(self, user):
        gallery = Gallery.objects.filter(user__id=user.id).prefetch_related('storage_backend').first()
        
        if gallery is None:
            storage_backend = StorageBackend.objects.filter(user__id=user.id).first()
            
            gallery = Gallery()
            gallery.name = 'My gallery' # Default gallery, for now
            gallery.storage_backend = storage_backend
            gallery.user = user
            # Create a folder for this gallery as a subfolder of the root folder
            folder_id = self.create_gallery_folder(gallery.name, storage_backend)
            
            if folder_id is None:
                print('Could not create folder for new gallery')
                return
            
            gallery.folder_id = folder_id
            gallery.save()
        
        print('gallery:')
        print(gallery)
        
        return gallery
    
    def create_gallery_folder(self, name, storage_backend):
        service = get_drive_service(
            storage_backend.meta['access_token'],
            storage_backend.meta['refresh_token'],
        )

        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [storage_backend.root_folder_id]
        }
        
        folder = service.files().create(body=file_metadata, fields='id').execute()
        
        print('Created folder for the new gallery:')
        print(folder)
        
        return folder['id']
    
    def upload(self, gallery, target_file):
        try:
            service = get_drive_service(
                gallery.storage_backend.meta['access_token'],
                gallery.storage_backend.meta['refresh_token'],
            )
        
            file_metadata = {
                'name': target_file.name,
                'parents': [gallery.folder_id]
            }
            
            f = io.BytesIO(target_file.read())
            media = MediaIoBaseUpload(f, mimetype=get_mime_type(f))

            file = service.files().create(
                body=file_metadata, 
                media_body=media,
                fields='id, name, imageMediaMetadata, mimeType, thumbnailLink'
            ).execute()
        
            print(file)
            
            return file
        except HttpError as error:
            print(F'An error occurred: {error}')
            
        
    def create_image(self, gallery, file):
        img = Image()
        img.name = file['name']
        img.file_id = file['id']
        img.width = file['imageMediaMetadata']['width']
        img.height = file['imageMediaMetadata']['height']
        img.mime_type = file['mimeType']
        img.gallery = gallery
        img.save()
        
        return img