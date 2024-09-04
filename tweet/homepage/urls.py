from django.urls import path

from . import views 

app_name="homepage"
urlpatterns=[
    path("", views.view_posts, name='home'),
    path("search/", views.search, name='search'),
    path("explore/", views.view_explore, name='explore'),
]