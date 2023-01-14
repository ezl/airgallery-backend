from rest_framework import serializers

from galleries.models import Gallery, Image

class GallerySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)

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
