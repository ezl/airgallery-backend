from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            return ValueError('Email is missing')

        user = self.model(email=self.normalize_email(email))
        
        if password is None:
            user.set_password(password)
            
        user.save(uaing=self._db)

        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    profile_picture_url = models.CharField(max_length=250)
    auth_provider_name = models.CharField(max_length=250)
    auth_provider_user_id = models.CharField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'

    objects = UserManager()
    
    class Meta():
        constraints = [
            models.UniqueConstraint(
                fields=['auth_provider_name', 'auth_provider_user_id'],
                name='users.auth_provider_name_auth_provider_user_id_unique'
            )
        ]