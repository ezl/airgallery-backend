from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture_url = models.CharField(max_length=250)
    auth_provider_name = models.CharField(max_length=250)
    auth_provider_user_id = models.CharField(max_length=250)

def set_user_profile_info(user, auth_provider_name, user_data):
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    user_profile.auth_provider_name = auth_provider_name
    user_profile.auth_provider_user_id = user_data['id']
    user_profile.profile_picture_url = user_data['picture']
    user_profile.save()

    user = user.user_profile
    user.first_name = user_data['given_name']
    user.last_name = user_data['family_name']
    user.email = user_data['email']
    user.save()

    return user_profile

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()

post_save.connect(create_profile, sender=User)
