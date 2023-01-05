from django.db import models
from django.utils import timezone

class StorageBackend(models.Model):
    name = models.CharField(max_length=250)
    meta = models.JSONField()
    root_folder_id = models.CharField(max_length=250)
    user = models.ForeignKey(to='base.User', on_delete = models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'storage_backends'
