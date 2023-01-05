from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture_url = models.CharField(max_length=250)
    auth_provider_name = models.CharField(max_length=250)
    auth_provider_user_id = models.CharField(max_length=250)

