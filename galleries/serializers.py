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

class GalleryCreateSerializer(serializers.Serializer):
    #WIP: made with Robert. Not in use.
    name = serializers.CharField()

class GalleryUpdateSerializer(serializers.Serializer):
    #WIP: made with Robert. Not in use.
    name = serializers.CharField()
    is_published = serializers.BooleanField()
    slug = serializers.CharField()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
