from rest_framework import serializers

from galleries.models import Gallery, Image
from user_profiles.serializers import UserSerializer

class GallerySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Gallery
        fields = [
            'id',
            'name',
            'slug',
            'user',
            'published_at',
        ]

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
