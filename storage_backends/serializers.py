from rest_framework import serializers

from .models import StorageBackend


class StorageBackendSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageBackend
        fields = '__all__'

