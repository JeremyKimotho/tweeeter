import datetime 

from django.contrib import admin 
from django.db import models
from django.utils import timezone 

from user_profile.models import UserProfile

class Post(models.Model): 
    poster = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.CharField(max_length=240)
    likes = models.IntegerField(default=0)
    quotes = models.IntegerField(default=0) 
    comments = models.IntegerField(default=0) 
    reposts = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)

class Quote(Post):
    quote_post = models.ForeignKey(Post, related_name='post_og_quote', on_delete=models.CASCADE)
    
class Comment(Post):
    reply_post = models.ForeignKey(Post, related_name='post_og_comment', on_delete=models.CASCADE) 
# Create your models here.
