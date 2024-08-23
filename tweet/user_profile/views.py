from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse 

from posts.models import Comment
from posts.models import Post
from posts.models import Quote    
from users.models import CustomUser
from user_profile.models import UserProfile


@login_required
def view_profile(request, profile_id):
    user_a = get_object_or_404(UserProfile, id=profile_id)
    context = {
               "bio": user_a.bio,
               "followers": user_a.followers,
               "following:": user_a.following,
               "location": user_a.location,
               "display_picture": user_a.display_picture,
               "display_name": user_a.display_name,
               "background": user_a.background_picture}
    return render(request, "view_profile.html", context)


@login_required
def view_user_following(request, profile_id):
    user_profile = get_object_or_404(UserProfile, id=profile_id)
    following = user_profile.following.all()
    context = {"latest_following_list": following}
    return render(request, "view_friends.html", context)


@login_required
def view_user_followers(request, profile_id):
    user_profile = get_object_or_404(UserProfile, id=profile_id)
    followers = user_profile.followers.all()
    context = {"latest_followers_list": followers}
    return render(request, "view_friends.html", context)


@login_required
def view_user_posts(request, profile_id):
    latest_posts_list = Post.objects.filter(poster_id=profile_id)
    context = {"latest_posts_list": latest_posts_list}
    return render(request, "posts.html", context)


@login_required
def view_user_quotes(request, profile_id):
    latest_quotes_list = Quote.objects.filter(poster_id=profile_id)
    context = {"latest_quotes_list": latest_quotes_list}
    return render(request, "posts.html", context)


@login_required
def view_user_comments(request, profile_id):
    latest_comments_list = Comment.objects.filter(poster_id=profile_id)
    context = {"latest_comments_list": latest_comments_list}
    return render(request, "posts.html", context)


@login_required
def view_user_reposts(request, profile_id):
    latest_reposts_list = Post.objects.filter(reposts__id=profile_id)
    context = {"latest_reposts_list": latest_reposts_list}
    return render(request, "posts.html", context)


@login_required
def view_user_likes(request, profile_id):
    latest_likes_list = Post.objects.filter(likes__id=profile_id)
    context = {"latest_likes_list": latest_likes_list}
    return render(request, "posts.html", context)


@login_required
def view_user_bookmarks(request):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    latest_bookmarks_list = Post.objects.filter(bookmarks__id=requester.id)
    context = {"latest_bookmarks_list": latest_bookmarks_list}
    return render(request, "posts.html", context)


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
        return HttpResponse()


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
        return HttpResponse()


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


# def view_user_dp(request, profile_id):
#     user = get_object_or_404(UserProfile, id=user_id)
#     return render(request, "display_picture.html", {"image": user.display_picture})


# def user_media(request, profile_id):
#     pass

    

