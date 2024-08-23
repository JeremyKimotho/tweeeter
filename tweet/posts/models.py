import datetime 

from django.contrib import admin 
from django.db import models
from django.utils import timezone 

from user_profile.models import UserProfile

class Post(models.Model): 
    poster = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.CharField(max_length=240)
    likes = models.ManyToManyField(UserProfile, blank=True, related_name='post_likes')
    reposts = models.ManyToManyField(UserProfile, blank=True, related_name='post_reposts')
    bookmarks = models.ManyToManyField(UserProfile, blank=True, related_name='post_bookmarkers') 
    quotes = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='post_quotes') 
    comments = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='post_comments')
    date_posted = models.DateTimeField(default=timezone.now)

class Quote(Post):
    quote_post = models.ForeignKey(Post, related_name='post_og_quote', on_delete=models.CASCADE)
    
class Comment(Post):
    reply_post = models.ForeignKey(Post, related_name='post_og_comment', on_delete=models.CASCADE) 
# Create your models here.
