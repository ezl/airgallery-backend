from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class StorageBackend(models.Model):
    name = models.CharField(max_length=250)
    meta = models.JSONField()
    root_folder_id = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'storage_backends'
