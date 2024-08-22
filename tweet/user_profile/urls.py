from django.urls import path

from . import views 

app_name="profile"
urlpatterns=[
    path("<int:profile_id>/home/", views.view_profile, name='home'),
    path("<int:profile_id>/following/", views.view_user_following, name='following'),
    path("<int:profile_id>/followers/", views.view_user_followers, name='followers'),
    path("<int:profile_id>/posts/", views.view_user_posts, name='posts'),
    path("<int:profile_id>/quotes/", views.view_user_quotes, name='quotes'),
    path("<int:profile_id>/comments/", views.view_user_comments, name='comments'),
    path("<int:profile_id>/reposts/", views.view_user_reposts, name='reposts'),
    path("<int:profile_id>/likes/", views.view_user_likes, name='likes'),
    path("<int:profile_id>/create-follow/", views.create_follow, name='create_follow'),
    path("<int:profile_id>/delete-follow/", views.delete_follow, name='delete_follow'),
    path("<int:profile_id>/remove-follow/", views.remove_follow, name='remove_follow'),
    path("bookmarks/", views.view_user_bookmarks, name='bookmarks'),
]