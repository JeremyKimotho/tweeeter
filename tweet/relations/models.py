from django.db import models

from django.db import models
from django.utils import timezone

from user_profile.models import UserProfile

class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='profile_follower')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='profile_following')
    mutual = models.BooleanField(default=False)

