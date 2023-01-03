import magic
import environ
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

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

    print('Created folder for the new gallery:')
    print(folder)

    return folder['id']
