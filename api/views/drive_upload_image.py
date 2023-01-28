from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from storage_backends.models import StorageBackend
from galleries.models import Gallery
from galleries.models import Image
# from api.helpers import get_drive_service, drive_create_folder


class DriveUploadImage(APIView):
    def post(self, request):
        gallery_slug = request.POST.get("gallery_slug")

        # gallery = get_object_or_404(Gallery, slug=gallery_slug)
        gallery = Gallery.objects.all()[0]

        file = request.FILES.get('file')

        new_file = gallery.add_image(file)
        return Response(data=new_file)


