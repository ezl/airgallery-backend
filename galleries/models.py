from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.models import TimeStampedModel

from storage_backends.models import StorageBackend


# class GalleryManager(models.Manager):
#     def create(self, **obj_data):
#         raise Exception("not yet implemented")
#         """
#         Extending the default create method because we want a gallery to
#         ALWAYS be created with the appropriate storage service in place
#         """
#         user = obj_data['user']
#
#         obj_data['storage_backend']
#         obj_data['']
#
#         return super().create(**obj_data)



class Gallery(TimeStampedModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=250)
    storage_backend = models.ForeignKey(to=StorageBackend, on_delete = models.CASCADE)
    folder_id = models.CharField(max_length=250)
    slug = models.CharField(max_length=250) #will we want to autoslugify this thing?
    published_at = models.DateTimeField(blank=True, null=True) #questionable whether we'll keep this field, at least like this

    def fetch_images(self):
        """
        Retrieve image files from this gallery’s remote storage folder
        """

        drive_service = self.storage_backend.get_drive_service()
        query = f"parents = '{self.folder_id}'"
        fields = 'files(id, name, imageMediaMetadata, thumbnailLink)'
        response = drive_service.files().list(q=query, fields=fields).execute()
        files = response.get('files', [])
        return files


class Image(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete = models.CASCADE)
    name = models.CharField(max_length=250)
    file_id = models.CharField(max_length=250)
    width = models.IntegerField()
    height = models.IntegerField()
    mime_type = models.CharField(max_length=250)
    # future probably adding attributes for the google path, references to other things like thumbnails, optimized versions, likes, comments
