from django.db import models

from posts.models import Post
from user_profile.models import UserProfile

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liker = models.ForeignKey(UserProfile, related_name='post_liker', on_delete=models.CASCADE)
    poster = models.ForeignKey(UserProfile, related_name='post_og_like', on_delete=models.CASCADE)

class Repost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reposter = models.ForeignKey(UserProfile, related_name='post_reposter', on_delete=models.CASCADE)
    poster = models.ForeignKey(UserProfile, related_name='post_og_repost', on_delete=models.CASCADE)
    
class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    bookmarker = models.ForeignKey(UserProfile, related_name='post_commenter', on_delete=models.CASCADE)
    poster = models.ForeignKey(UserProfile, related_name='post_og_comment', on_delete=models.CASCADE)

