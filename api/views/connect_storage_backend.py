from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from base.models.storage_backend import StorageBackend
from api.helpers import (
        get_drive_service,
        drive_create_folder,
        exchange_authorization_code_for_access_token,
        get_user_info,
        create_backend_storage_if_new,
        create_gallery
    )



class ConnectStorageBackend(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):

        grant = exchange_authorization_code_for_access_token(request.data['code'])

        if grant is None:
            return Response('Invalid code', status=status.HTTP_400_BAD_REQUEST)

        # Let the client know the user didn’t grant us access to his Drive
        if 'https://www.googleapis.com/auth/drive' not in grant['scope']:
            return Response(
                {
                'missing_permission_google_dive': True,
                },
                 status=status.HTTP_400_BAD_REQUEST
            )

        user_info = get_user_info(grant['access_token'])

        if user_info is None:
            return Response('Could not get user info', status=status.HTTP_400_BAD_REQUEST)

        user, user_created = User.objects.get_or_create(username=user_info['email'])
        if user_created is True:
            user.email = user.username
            user.save()

        if not StorageBackend.objects.filter(user=user).exists():
            folder_id = drive_create_folder(
                'universal-photo-gallery',
                grant['access_token'],
                grant['refresh_token'],
                )

            storage_backend = StorageBackend.objects.get_or_create(
                user=user,
                name='google-drive',
                root_folder_id=folder_id,
                meta=grant
                )

            create_gallery(storage_backend, user, gallery_name='My Gallery')

        refreshToken = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refreshToken.access_token),
        })



