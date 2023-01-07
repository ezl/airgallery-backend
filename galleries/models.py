from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.models import TimeStampedModel

from storage_backends.models import StorageBackend


class Gallery(TimeStampedModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    storage_backend = models.ForeignKey(to=StorageBackend, on_delete = models.CASCADE)
    name = models.CharField(max_length=250)
    folder_id = models.CharField(max_length=250)
    slug = models.CharField(max_length=250) #will we want to autoslugify this thing?
    published_at = models.DateTimeField(blank=True, null=True) #questionable whether we'll keep this field, at least like this


class Image(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete = models.CASCADE)
    name = models.CharField(max_length=250)
    file_id = models.CharField(max_length=250)
    width = models.IntegerField()
    height = models.IntegerField()
    mime_type = models.CharField(max_length=250)
    # future probably adding attributes for the google path, references to other things like thumbnails, optimized versions, likes, comments
