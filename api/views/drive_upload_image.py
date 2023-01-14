from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from storage_backends.models import StorageBackend
from galleries.models import Gallery
from galleries.models import Image
# from api.helpers import get_drive_service, drive_create_folder


class DriveUploadImage(APIView):
    def put(self, request):
        print("1" * 50)
        gallery = Gallery.objects.filter(user__id=request.user.id).prefetch_related('storage_backend').first()

        if gallery is None:
            return Response('Default gallery not found', status=status.HTTP_404_NOT_FOUND)

        file = request.FILES['image']

        new_file = gallery.add_image(file)

        return Response(data=new_file)


