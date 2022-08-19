from django.db import models
from django.utils import timezone

class Image(models.Model):
    name = models.CharField(max_length=250)
    file_id = models.CharField(max_length=250)
    width = models.IntegerField()
    height = models.IntegerField()
    mime_type = models.CharField(max_length=250)
    gallery = models.ForeignKey(to='base.Gallery', on_delete = models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
        
    class Meta():
        db_table = 'images'