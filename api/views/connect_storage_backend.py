from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import User, Gallery
from base.models.user import find_or_create_user
from rest_framework_simplejwt.tokens import RefreshToken
import environ
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from api.helpers import (
        get_drive_service,
        drive_create_folder,
        exchange_authorization_code_for_access_token,
        get_user_info,
        create_backend_storage_if_new,
        create_gallery
    )


import uuid


env = environ.Env()

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

        user = find_or_create_user('google', user_info)

        create_backend_storage_if_new(
            'google-drive',
            user,
            grant
        )

        refreshToken = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refreshToken.access_token),
        })



