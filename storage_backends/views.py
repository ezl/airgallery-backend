from rest_framework import viewsets
from rest_framework import permissions

from .models import StorageBackend
from .serializers import StorageBackendSerializer


class StorageBackendViewSet(viewsets.ModelViewSet):
    queryset = StorageBackend.objects.all()
    serializer_class = StorageBackendSerializer
    permission_classes = [permissions.AllowAny]


