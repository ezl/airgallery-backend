from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.models import TimeStampedModel


class StorageBackend(TimeStampedModel):
    name = models.CharField(max_length=255)
    meta = models.JSONField()
    root_folder_id = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
