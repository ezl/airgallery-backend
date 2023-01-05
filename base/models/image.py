from django.db import models
from django.utils import timezone
from base.models.gallery import Gallery

class Image(models.Model):
    name = models.CharField(max_length=250)
    file_id = models.CharField(max_length=250)
    width = models.IntegerField()
    height = models.IntegerField()
    mime_type = models.CharField(max_length=250)
    gallery = models.ForeignKey(Gallery, on_delete = models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
