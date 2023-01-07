from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from storage_backends.models import StorageBackend

class Gallery(models.Model):
    name = models.CharField(max_length=250)
    folder_id = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    published_at = models.DateTimeField(blank=True, null=True)
    storage_backend = models.ForeignKey(to=StorageBackend, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
