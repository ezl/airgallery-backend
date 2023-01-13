import requests

from storage_backends.models import StorageBackend
from galleries.models import Gallery

import environ
env = environ.Env()


"""
Steps in order:
    1. exchange authorziation_code for access token
    2. get_user_info
"""

class Google(object):
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.refresh_token = None
        self.scope = []
        self.user_info = {}

    def authenticate(self, code):
        """
        Give Google an authorization code, get auth data in return.
        """
        url = 'https://accounts.google.com/o/oauth2/token'
        grandType = 'authorization_code' #TODO: "grand type" seems fishy.
        payload = {
            'client_id': env('GOOGLE_CLIENT_ID'),
            'client_secret': env('GOOGLE_CLIENT_SECRET'),
            'grant_type': grandType,
            'redirect_uri': env('GOOGLE_REDIRECT_URL'),
            'code': code
        }
        response = requests.post(url=url, params=payload)

        if response.status_code != 200:
            raise Exception("Unable to authenticate via Google: {}".format(response))

        data = response.json()
        self.scope = data['scope']
        self.access_token= data['access_token']

        if not self.has_required_scope():
            raise Exception('Missing required scope: auth/drive')

        return data

    def has_required_scope(self):
        """
        Check to see if our current instance has the required scope
        in order to function for this gallery (basically Google Drive
        access)
        """
        REQUIRED_SCOPES = [
            'https://www.googleapis.com/auth/drive'
            ]
        return all([item in self.scope for item in REQUIRED_SCOPES])


    def get_user_info(self):
        if self.access_token is None:
            raise Exception("Not authenticated")

        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        headers = {
            'Authorization': 'Bearer ' + self.access_token
        }

        response = requests.get(url=url, headers=headers)

        if response.status_code != 200:
            raise Exception("Unable to get Google user info")

        data = response.json()
        self.user_info = data
        print(self.user_info)
        return self.user_info



