import uuid
import environ
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from storage_backends.models import StorageBackend
from user_profiles.models import UserProfile
from galleries.models import Gallery

from api.helpers import Google

env = environ.Env()

class ConnectStorageBackend(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        google = Google(
                    env('GOOGLE_CLIENT_ID'),
                    env('GOOGLE_CLIENT_SECRET')
                    )

        auth_data = google.authenticate(request.data['code'])

        user_info = google.get_user_info()
        user, user_created = User.objects.get_or_create(username=user_info['email'])

        if user_created is True:
            user.first_name = user_info['given_name']
            user.last_name = user_info['family_name']
            user.email = user.username
            user.save()

            user_profile = UserProfile.objects.create(
                    user=user,
                    auth_provider_name='google',
                    auth_provider_user_id=user_info['id'],
                    profile_picture_url=user_info['picture']
                )

        if not StorageBackend.objects.filter(user=user).exists():
            # create the root folder
            storage_backend = StorageBackend(
                user=user,
                name='google-drive',
                meta=auth_data
                )
            ROOT_FOLDER_NAME = 'universal-photo-gallery'
            root_folder_id = storage_backend.create_folder(ROOT_FOLDER_NAME)
            storage_backend.root_folder_id = root_folder_id
            storage_backend.save()

            # create the gallery folder inside the root of google drive

            # TODO: need to make gallery creation and folder creation happen together as a transaction
            gallery_name = 'My Gallery'
            gallery_folder_id = storage_backend.create_folder(gallery_name, parent=root_folder_id)
            gallery = Gallery.objects.create(
                    user=user,
                    name=gallery_name,
                    storage_backend=storage_backend,
                    folder_id=gallery_folder_id,
                    slug=uuid.uuid4()
                    )

        refreshToken = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refreshToken.access_token),
        })



