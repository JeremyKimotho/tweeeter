from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

def validate_file_type(value):
    valid_mime_types = [
        'image/jpeg', 'image/png', 'image/gif',  # Images
        'video/mp4', 'video/mpeg', 'video/avi', 'video/webm'  # Videos
    ]
    file_type = value.file.content_type
    if file_type not in valid_mime_types:
        raise ValidationError(f'Unsupported file type: {file_type}')



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=20, default='Mars')
    followers = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='user_followers') 
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='user_following') 
    display_picture = models.CharField(default='user1.avif')
    display_name = models.CharField(max_length=18, default='New User')
    bio = models.CharField(max_length=80, default='I\'m new here ! :)')
    background_picture = models.CharField(default='background1.jpg')
    blocked_list = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='user_blocks')
    muted_list = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='user_muted')

    def getFollowers(self):
        return self.followers.count()
    
    def getFollowing(self):
        return self.following.count()