import environ

from django.db import models
from django.contrib.auth.models import User
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from django_extensions.db.models import TimeStampedModel

env = environ.Env()


class StorageBackend(TimeStampedModel):
    name = models.CharField(max_length=255)
    meta = models.JSONField()
    root_folder_id = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def get_drive_service(self, access_token=None, refresh_token=None):
        ACCESS_TOKEN = access_token or self.meta.get('access_token')
        REFRESH_TOKEN = refresh_token or self.meta.get('refresh_token')

        if (ACCESS_TOKEN is None) or (REFRESH_TOKEN is None):
            raise Exception("No access or refresh token: Unable to get drive service.")

        creds = Credentials(
            token_uri='https://accounts.google.com/o/oauth2/token',
            token=ACCESS_TOKEN,
            refresh_token=REFRESH_TOKEN,
            client_id=env('GOOGLE_CLIENT_ID'),
            client_secret=env('GOOGLE_CLIENT_SECRET')
            )
        drive_service = build('drive', 'v3', credentials=creds)
        return drive_service

    def create_folder(self, name, parent=None):
        drive_service = self.get_drive_service()

        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
        }

        if parent is not None:
            file_metadata['parents'] = [parent]

        folder = drive_service.files().create(body=file_metadata, fields='id').execute()

        if folder['id'] is None:
            raise Exception('Could not create root folder')

        return folder['id']

