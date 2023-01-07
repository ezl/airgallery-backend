from rest_framework import serializers
from galleries.models import Gallery
from api.serializers import UserSerializer

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

