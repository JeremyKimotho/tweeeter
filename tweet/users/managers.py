from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from user_profile.models import UserProfile

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The email must be set"))
        email = self.normalize_email(email=email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        # Create profile automatically at user creation
        user_profile = UserProfile.objects.create(user = user)
        user_profile.save()

        return user 
    
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_admin  = True
        user.is_staff = True
        user.is_superuser = True
        return user
