from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from base.models import User, StorageBackend
from rest_framework_simplejwt.tokens import RefreshToken
import environ

env = environ.Env() 

class ConnectStorageBackend(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request, format=None):

        grant = self.exchange_authorization_code_for_access_token(request.data['code'])
        
        if grant is None:
            return Response('Invalid code', status=status.HTTP_400_BAD_REQUEST)
    
        user_info = self.get_user_info(grant['access_token'])
        
        if user_info is None:
            return Response('Could not get user info', status=status.HTTP_400_BAD_REQUEST)
        
        user = self.find_or_create_user('google', user_info)
        
        self.create_backend_storagr_if_new(
            'google-drive',
            user,
            grant
        )
                
        refreshToken = RefreshToken.for_user(user)
    
        return Response({
            'access_token': str(refreshToken.access_token),
        })
    
    def exchange_authorization_code_for_access_token(self, code):
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
        
    def get_user_info(self, token):
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'        
        headers = {
            'Authorization': 'Bearer ' + token
        }
        
        res = requests.get(url=url, headers=headers)
        
        if res.status_code != 200:
            return
        
        return res.json()
        
    def find_or_create_user(self, auth_provider_name, user_data):
        user = User.objects.filter(
            auth_provider_name=auth_provider_name,
            auth_provider_user_id=user_data['id']
        ).first()
        
        if user is None:
            password = User.objects.make_random_password()    
            user = User()
            user.password = password
            user.auth_provider_name = auth_provider_name
            user.auth_provider_user_id = user_data['id']
            user.first_name = user_data['given_name']
            user.last_name = user_data['family_name']
            user.profile_picture_url = user_data['picture']
            user.email = user_data['email']
            user.save()
        

        return user
    
    def create_backend_storagr_if_new(self, name, user, grant):
        already_connected = StorageBackend.objects.filter(user__id=user.id).exists()
        
        if already_connected:
            return
        
        meta = {
            'access_token': grant['access_token'],
            'refresh_token': grant['refresh_token'],
        }
        
        storage_backend = StorageBackend()
        storage_backend.name = name
        storage_backend.meta = meta
        storage_backend.user = user
        storage_backend.save()
        
        return storage_backend