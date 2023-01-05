import uuid
import magic
import environ
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from base.models.storage_backend import StorageBackend
from base.models.gallery import Gallery

env = environ.Env()

def get_drive_service(access_token, refresh_token):
    creds = Credentials(
        token_uri='https://accounts.google.com/o/oauth2/token',
        token=access_token,
        refresh_token=refresh_token,
        client_id= env('GOOGLE_CLIENT_ID'),
        client_secret= env('GOOGLE_CLIENT_SECRET'),
    )

    service = build('drive', 'v3', credentials=creds)

    return service


def get_mime_type(file):
    """
    Get MIME by reading the header of the file
    """
    initial_pos = file.tell()
    file.seek(0)
    mime_type = magic.from_buffer(file.read(2048), mime=True)
    file.seek(initial_pos)
    return mime_type

def fetchGalleryImages(gallery):
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

def drive_create_folder(name, access_token, refresh_token, parent=None):
    service = get_drive_service(
        access_token,
        refresh_token,
    )

    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
    }

    if parent is not None:
        file_metadata['parents'] = [parent]

    folder = service.files().create(body=file_metadata, fields='id').execute()

    if folder['id'] is None:
        raise Exception('Could not create root folder')

    return folder['id']

def exchange_authorization_code_for_access_token(code):
    url = 'https://accounts.google.com/o/oauth2/token'
    grandType = 'authorization_code'

    payload = {
        'client_id': env('GOOGLE_CLIENT_ID'),
        'client_secret': env('GOOGLE_CLIENT_SECRET'),
        'grant_type': grandType,
        'redirect_uri': env('GOOGLE_REDIRECT_URL'),
        'code': code
    }

    res = requests.post(url=url, params=payload)

    if res.status_code != 200:
        return

    return res.json()


def get_user_info(token):
    url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {
        'Authorization': 'Bearer ' + token
    }

    res = requests.get(url=url, headers=headers)

    if res.status_code != 200:
        return

    return res.json()


def create_gallery(storage_backend, user, gallery_name):
    gallery = Gallery()
    gallery.name = gallery_name
    gallery.slug = uuid.uuid4()
    gallery.storage_backend = storage_backend
    gallery.user = user

    # Create a folder for this gallery as a subfolder of the root folder
    folder_id = drive_create_folder(
        gallery.name,
        storage_backend.meta['access_token'],
        storage_backend.meta['refresh_token'],
        storage_backend.root_folder_id
    )

    if folder_id is None:
        #TODO this print statement will break in production
        print('Could not create folder for new gallery')
        return

    gallery.folder_id = folder_id
    gallery.save()

    return gallery
