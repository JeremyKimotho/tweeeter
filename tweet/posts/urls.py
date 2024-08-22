from django.urls import path

from . import views 

app_name="posts"
urlpatterns=[
    path("<int:post_id>/", views.display_post),
    path("<int:post_id>/repost/", views.create_repost, name='repost'),
    path("<int:post_id>/unrepost/", views.delete_repost, name='unrepost'),
    path("<int:post_id>/like/", views.create_like, name='like'),
    path("<int:post_id>/unlike/", views.delete_like, name='unlike'),
    path("<int:post_id>/quote/", views.create_quote, name='quote'),
    path("<int:post_id>/unquote/", views.delete_quote, name='unquote'),
    path("<int:post_id>/comment/", views.create_comment, name='comment'),
    path("<int:post_id>/uncomment/", views.delete_comment, name='uncomment'),
    path("<int:post_id>/bookmark/", views.create_bookmark, name='bookmark'),
    path("<int:post_id>/unbookmark/", views.delete_bookmark, name='unbookmark'),
    path("<int:post_id>/unpost/", views.delete_post, name='unpost'),
    path("create-post/", views.create_post, name='create_post'),
]