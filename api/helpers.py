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