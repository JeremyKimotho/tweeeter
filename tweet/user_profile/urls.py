from django.urls import path

from . import views 

app_name="profile"
urlpatterns=[
    path("home/<int:profile_id>/", views.view_profile, name='home'),
    path("following/<int:profile_id>/", views.view_user_following, name='following'),
    path("followers/<int:profile_id>/", views.view_user_followers, name='followers'),
    path("posts/<int:profile_id>/", views.view_user_posts, name='posts'),
    path("quotes/<int:profile_id>/", views.view_user_quotes, name='quotes'),
    path("comments/<int:profile_id>/", views.view_user_comments, name='comments'),
    path("reposts/<int:profile_id>/", views.view_user_reposts, name='reposts'),
    path("likes/<int:profile_id>/", views.view_user_likes, name='likes'),
    path("media/<int:profile_id>/", views.view_user_media, name='media'),
    path("create-follow/<int:profile_id>/", views.create_follow, name='create_follow'),
    path("delete-follow/<int:profile_id>/", views.delete_follow, name='delete_follow'),
    path("remove-follow/<int:profile_id>/", views.remove_follow, name='remove_follow'),
    path("view-profile/<int:profile_id>/", views.view_profile, name='view_profile'),
    path("view-profile/", views.view_own_profile, name='my_profile'),
    path("edit-profile/", views.edit_profile, name='edit_profile'),
    path("bookmarks/", views.view_user_bookmarks, name='bookmarks'),
    path("messages/", views.view_messages, name='view_messages'),
    path("notifications/", views.view_notifications, name='notifications'),
    path("go-back", views.go_back, name="back"),
    path("manage-follows/<int:profile_id>/", views.manage_follows, name="follow_user"),
    path("block-profile/<int:profile_id>/", views.block_profile, name='block'),
    path("mute-profile/<int:profile_id>/", views.mute_profile, name='mute'),
]