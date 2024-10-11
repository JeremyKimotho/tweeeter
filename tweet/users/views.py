from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse 
   
from users.models import CustomUser
from user_profile.models import UserProfile

from .templates.forms import CustomUserCreationForm

@login_required
def view_account_details():
    pass

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            new_user = CustomUser.objects.create_user(
                email=form.cleaned_data['email'],
                user_name=form.cleaned_data['user_name'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                password=form.cleaned_data['password1'],
            )

            login(request, new_user)
            return HttpResponse(status=204)
        else:
            # Check for specific errors and replace them
            if "Custom user with this Email address already exists." in form.errors.get("email", []):
                form.errors["email"] = ["Account with this email address already exists."]
            if "Custom user with this User name already exists." in form.errors.get("user_name", []):
                form.errors["user_name"] = ["This username is taken."]
    # if a GET (or anything other than POST), create blank form
    else:
        form = CustomUserCreationForm()

    return render(request,  "registration/registration_page.html", {"form": form})

@login_required
def delete_user():
    pass

@login_required
def change_account_details():
    pass