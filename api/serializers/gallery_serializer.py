from rest_framework import serializers
from base.models import Gallery
from . import UserSerializer

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

