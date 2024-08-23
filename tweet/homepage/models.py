from django.db import models
from django.utils import timezone 

from posts.models import Post
from user_profile.models import UserProfile

class PostTraction(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    score = models.FloatField(default=1)
    pub_date = models.DateTimeField(default=timezone.now)
    poster = models.ForeignKey(UserProfile, on_delete=models.CASCADE)