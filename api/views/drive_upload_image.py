from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from storage_backends.models import StorageBackend
from galleries.models import Gallery
from galleries.models import Image
# from api.helpers import get_drive_service, drive_create_folder
from api.helpers import get_mime_type
from api.helpers import Google
import io

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

class DriveUploadImage(APIView):
    def put(self, request):
        gallery = Gallery.objects.filter(user__id=request.user.id).prefetch_related('storage_backend').first()

        if gallery is None:
            return Response('Default gallery not found', status=status.HTTP_404_NOT_FOUND)

        file = request.FILES['image']

        new_file = self.upload(gallery, file)

        self.create_image(gallery, new_file)

        return Response(data=new_file)

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
