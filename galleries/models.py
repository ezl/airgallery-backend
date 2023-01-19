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

    def add_image(self, target_file):
        '''
        Need to:
        (A) upload the image to remote storage
        (B) create the image object with meta data
        '''
        # Upload the image
        image_file = self.storage_backend.upload_image(target_file, self)

        # Create the image asset
        image = Image.objects.create(
            name           = image_file['name'],
            file_id        = image_file['id'],
            width          = image_file['imageMediaMetadata']['width'],
            height         = image_file['imageMediaMetadata']['height'],
            mime_type      = image_file['mimeType'],
            gallery        = self
            )
        return image_file

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


class Image(TimeStampedModel):
    name = models.CharField(max_length=250)
    gallery = models.ForeignKey(Gallery, on_delete = models.CASCADE)
    height = models.IntegerField()
    width = models.IntegerField()
    file_id = models.CharField(max_length=250) # TODO:file_id will probably generalized to something else if we go to multiple storage backends
    mime_type = models.CharField(max_length=250) # TODO:mime_Type -- why is this necessary? If generalized, will this live in some other metadata json blob?
    # future probably adding attributes for the google path, references to other things like thumbnails, optimized versions, likes, comments

