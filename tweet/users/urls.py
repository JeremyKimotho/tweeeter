from django.contrib.auth import views as auth_views
from django.urls import path
from .templates.forms import CustomAuthenticationForm

from . import views 

app_name="users"
urlpatterns=[
    path("login/", auth_views.LoginView.as_view(
        authentication_form=CustomAuthenticationForm
    ),name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("registration/", views.register_user, name="registration"),
    path("details/", views.view_account_details, name="account_details"),
    path("search-usernames/", views.search_usernames, name='search_usernames')
]