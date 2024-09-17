import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse 
from urllib.parse import urlparse

from .templates.forms.profile_change_form import ProfileChangeForm
from homepage.views import create_combined_posts, create_combined_profile, create_combined_profiles
from posts.models import BasePost, Comment, Post, Quote   
from users.models import CustomUser
from user_profile.models import UserProfile

@login_required
def view_profile(request, profile_id):
    return redirect(reverse('profile:posts', args=(profile_id,)))

@login_required
def view_own_profile(request):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    user_profile = get_object_or_404(UserProfile, user_id=requester_cu.id)

    return redirect(reverse('profile:posts', args=(user_profile.id,)))

@login_required
def view_user_following(request, profile_id):
    user_profile = get_object_or_404(UserProfile, id=profile_id)
    user_account = get_object_or_404(CustomUser, id=user_profile.user_id)
    following = user_profile.following.all()

    latest_following = create_combined_profiles(request, following)
    user_profile = create_combined_profile(request, user_profile, user_account)

    context = {"latest_following_list": latest_following, "profile_data": user_profile, "profile": user_profile}
    return render(request, "view_following.html", context)


@login_required
def view_user_followers(request, profile_id):
    user_profile = get_object_or_404(UserProfile, id=profile_id)
    user_account = get_object_or_404(CustomUser, id=user_profile.user_id)
    followers = user_profile.followers.all()

    latest_followers = create_combined_profiles(request, followers)
    user_profile = create_combined_profile(request, user_profile, user_account)

    context = {"latest_followers_list": latest_followers,  "profile_data": user_profile, "profile": user_profile}
    return render(request, "view_followers.html", context)


@login_required
def view_user_posts(request, profile_id):
    user_profile  = get_object_or_404(UserProfile, id=profile_id)
    user_cu = get_object_or_404(CustomUser, id=user_profile.user_id)

    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)


    latest_posts_list_raw = Post.objects.filter(poster_id=profile_id)
    latest_quotes_list_raw = Quote.objects.filter(poster_id=profile_id)
    latest_posts_list = create_combined_posts(latest_posts_list_raw, requester)
    latest_quotes_list = create_combined_posts(latest_quotes_list_raw, requester)
    latest_posts_list += latest_quotes_list

    user_profile_stripped = create_combined_profile(request, user_profile, user_cu, len(latest_posts_list))

    context = {"latest_posts": latest_posts_list, "profile_data": user_profile_stripped, "profile": user_profile_stripped}
    return render(request, "posts.html", context)


@login_required
def view_user_quotes(request, profile_id):
    latest_quotes_list = Quote.objects.filter(poster_id=profile_id)
    context = {"latest_quotes_list": latest_quotes_list}
    return render(request, "posts.html", context)


@login_required
def view_user_comments(request, profile_id):
    user_profile  = get_object_or_404(UserProfile, id=profile_id)
    user_cu = get_object_or_404(CustomUser, id=user_profile.user_id)

    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    latest_comments_list_raw = Comment.objects.filter(poster_id=profile_id)
    latest_comments_list = create_combined_posts(latest_comments_list_raw, requester)

    user_profile_stripped = create_combined_profile(request, user_profile, user_cu)

    context = {"latest_posts": latest_comments_list, "profile_data": user_profile_stripped, "profile": user_profile_stripped}
    return render(request, "comments.html", context)


@login_required
def view_user_reposts(request, profile_id):
    latest_reposts_list = Post.objects.filter(reposts__id=profile_id)
    context = {"latest_reposts_list": latest_reposts_list,}
    return render(request, "posts.html", context)


@login_required
def view_user_likes(request, profile_id):
    user_profile  = get_object_or_404(UserProfile, id=profile_id)
    user_cu = get_object_or_404(CustomUser, id=user_profile.user_id)

    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    user_profile_stripped = create_combined_profile(request, user_profile, user_cu)

    latest_likes_list_raw_p = Post.objects.filter(likes__id=profile_id)
    latest_likes_list_raw_q = Quote.objects.filter(likes__id=profile_id)
    latest_likes_list_raw_c = Comment.objects.filter(likes__id=profile_id)
    latest_likes_list = create_combined_posts(latest_likes_list_raw_p, requester) + create_combined_posts(latest_likes_list_raw_q, requester) + create_combined_posts(latest_likes_list_raw_c, requester)

    context = {"latest_posts": latest_likes_list, "profile_data": user_profile_stripped, "profile": user_profile_stripped}
    return render(request, "likes.html", context)

@login_required
def view_user_media(request, profile_id):
    user_profile  = get_object_or_404(UserProfile, id=profile_id)
    user_cu = get_object_or_404(CustomUser, id=user_profile.user_id)

    user_profile_stripped = create_combined_profile(request, user_profile, user_cu)

    latest_media_list=[]

    context = {"latest_posts": latest_media_list, "profile_data": user_profile_stripped, "profile": user_profile_stripped}
    return render(request, "media.html", context)


@login_required
def view_user_bookmarks(request):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    latest_posts_raw = Post.objects.filter(bookmarks__id=requester.id)
    latest_quotes_raw = Quote.objects.filter(bookmarks__id=requester.id)
    latest_posts = create_combined_posts(latest_posts_raw, requester)
    latest_quotes = create_combined_posts(latest_quotes_raw, requester)
    latest_posts += latest_quotes

    context = {"latest_posts": latest_posts, "username": requester_cu.user_name, "profile": create_combined_profile(request, requester, requester_cu)}
    return render(request, "bookmarks.html", context)


@login_required
def manage_follows(request, profile_id):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)
    profile_to_follow = get_object_or_404(UserProfile, user_id=profile_id)

    # make sure not trying to follow self
    if requester.id == profile_id:
        return HttpResponseRedirect(reverse("profile:home", args=(profile_id,)))
    # if requester already follows, this is unfollow request
    elif requester.following.contains(profile_to_follow):
        return delete_follow(request, profile_id=profile_id)
    else:
        return create_follow(request, profile_id=profile_id)


@login_required
def create_follow(request, profile_id):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)
    profile_to_follow = get_object_or_404(UserProfile, user_id=profile_id)

    # make sure not trying to follow self
    if requester.id == profile_id:
        return HttpResponseRedirect(reverse("profile:home", args=(profile_id,)))
    else:
        requester.following.add(profile_to_follow)
        profile_to_follow.followers.add(requester)
        return HttpResponse("Following")


@login_required
def delete_follow(request, profile_id):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)
    profile_to_follow = get_object_or_404(UserProfile, user_id=profile_id)

    # make sure not trying to unfollow self
    if requester.id == profile_id:
        return HttpResponseRedirect(reverse('profile:home'), args=(profile_id,))
    else:
        requester.following.remove(profile_to_follow)
        profile_to_follow.followers.remove(requester)
        return HttpResponse("Follow")


@login_required
def remove_follow(request, profile_id):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)
    profile_to_follow = get_object_or_404(UserProfile, user_id=profile_id)

    # make sure not trying to remove self as follower
    if requester.id == profile_id:
        return HttpResponseRedirect(reverse('profile:home'), args=(profile_id,))
    else:
        requester.following.remove(profile_to_follow)
        requester.followers.remove(profile_to_follow)
        profile_to_follow.following.remove(requester)
        profile_to_follow.followers.remove(requester)

        return HttpResponse()

@login_required
def view_messages(request):
    pass

@login_required
def view_notifications(request):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    context = {"username": requester_cu.user_name, "profile": create_combined_profile(request, requester, requester_cu)}
    return render(request, "notifications.html", context)


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileChangeForm(request.POST)

        if form.is_valid():
            poster_cu = get_object_or_404(CustomUser, email=request.user.get_username())
            poster = get_object_or_404(UserProfile, user_id=poster_cu.id)

            if form.cleaned_data['display_name'] != None and form.cleaned_data['display_name'] != "":
                poster.display_name=form.cleaned_data['display_name']
            
            if form.cleaned_data['location'] != None and form.cleaned_data['location'] != "":
                poster.location=form.cleaned_data['location']

            if form.cleaned_data['bio'] != None and form.cleaned_data['bio'] != "":
                poster.bio=form.cleaned_data['bio']
                
            day = form.cleaned_data['day']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            poster_cu.date_of_birth=datetime.date(int(year),int(month),int(day))

            poster.save()
            poster_cu.save()

        return HttpResponse(status=204)
    
    else:
        user_cu = get_object_or_404(CustomUser, email=request.user.get_username())
        user_p = get_object_or_404(UserProfile, user_id=user_cu.id)
        user_profile_stripped = create_combined_profile(request, user_p, user_cu)

        form = ProfileChangeForm(initial={
            'display_name': user_profile_stripped['display_name'],
            'location': user_profile_stripped['location'],
            'month': user_profile_stripped['dob'].month,
            'day': user_profile_stripped['dob'].day,
            'year': user_profile_stripped['dob'].year,
        })

    return render(request, "profile_edit.html", {"form": form, "profile": user_profile_stripped})

# def view_user_dp(request, profile_id):
#     user = get_object_or_404(UserProfile, id=user_id)
#     return render(request, "display_picture.html", {"image": user.display_picture})


# def user_media(request, profile_id):
#     pass

def go_back(request):
    back_page = request.META.get('HTTP_REFERER')

    if back_page:
        bp_domain = urlparse(back_page).netloc
        current_domain = request.get_host()

        print(f"BP domain {bp_domain}, CD is {current_domain}")

        if bp_domain == current_domain:
            return redirect(back_page)
        
    return redirect(reverse('homepage:home'))

@login_required
def block_profile(request, profile_id):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)
    profile = get_object_or_404(UserProfile, id=profile_id)

    if requester != profile:   
        if request.method == "POST":
            requester.blocked_list.add(profile)
            return HttpResponse(status=204)

        return render(request, "block_profile.html", {"type":"block"})
    else:
        return redirect(reverse('homepage:home')) # homepage

@login_required
def mute_profile(request, profile_id):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)
    profile = get_object_or_404(UserProfile, id=profile_id)

    if requester != profile:   
        if request.method == "POST":
            requester.muted_list.add(profile)
            return HttpResponse(status=204)

        return render(request, "block_profile.html",)
    else:
        return redirect(reverse('homepage:home')) # homepage
    
