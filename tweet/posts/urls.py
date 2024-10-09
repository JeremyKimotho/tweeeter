from django.urls import path

from . import views 

app_name="posts"
urlpatterns=[
    path("view-post/<int:post_id>/<int:post_op_id>/", views.display_post, name='display_post'),
    path("create-repost/<int:post_id>/", views.create_repost, name='repost'),
    path("delete-repost/<int:post_id>/", views.delete_repost, name='unrepost'),
    path("create-like/<int:post_id>/", views.create_like, name='like'),
    path("delete-like/<int:post_id>/", views.delete_like, name='unlike'),
    path("create-quote/<int:post_id>/", views.create_quote, name='quote'),
    path("delete-quote/<int:post_id>/", views.delete_quote, name='unquote'),
    path("create-comment/<int:post_id>/", views.create_comment, name='comment'),
    path("delete-comment/<int:post_id>/", views.delete_comment, name='uncomment'),
    path("create-bookmark/<int:post_id>/", views.create_bookmark, name='bookmark'),
    path("delete-bookmark/<int:post_id>/", views.delete_bookmark, name='unbookmark'),
    path("delete-post/<int:post_id>/", views.delete_post, name='unpost'),
    path("create-post/", views.create_post, name='create_post'),
    path("get-comments-count/<int:post_id>/", views.get_comments_count, name="get_comments_count"),
    path("pin-post/<int:post_id>/", views.pin_post, name='pin_post'),
    path("view-quotes/<int:post_id>/", views.view_quotes, name='view_quotes'),
] 