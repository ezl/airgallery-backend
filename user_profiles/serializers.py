from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.CharField(read_only=True, source='user_profile.profile_picture_url')

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'profile_picture_url',
        ]


