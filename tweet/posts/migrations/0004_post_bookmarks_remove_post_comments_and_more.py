# Generated by Django 5.0.6 on 2024-08-23 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_poster'),
        ('user_profile', '0003_remove_userprofile_comments_remove_userprofile_likes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='post_bookmarkers', to='user_profile.userprofile'),
        ),
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='quotes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='reposts',
        ),
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='post_comments', to='posts.post'),
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='post_likes', to='user_profile.userprofile'),
        ),
        migrations.AddField(
            model_name='post',
            name='quotes',
            field=models.ManyToManyField(blank=True, related_name='post_quotes', to='posts.post'),
        ),
        migrations.AddField(
            model_name='post',
            name='reposts',
            field=models.ManyToManyField(blank=True, related_name='post_reposts', to='user_profile.userprofile'),
        ),
    ]
