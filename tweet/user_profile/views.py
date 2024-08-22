from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse 

from interactions.models import Like
from interactions.models import Repost
from interactions.models import Bookmark
from posts.models import Comment
from posts.models import Post
from posts.models import Quote    
from relations.models import Follow
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
    following_fo = Follow.objects.filter(follower_id=profile_id)
    following = [get_object_or_404(UserProfile, id=follow.following_id) for follow in following_fo]
    context = {"latest_following_list": following}
    return render(request, "view_friends.html", context)


@login_required
def view_user_followers(request, profile_id):
    followers_fo = Follow.objects.filter(following_id=profile_id)
    followers = [get_object_or_404(UserProfile, id=follower.follower_id) for follower in followers_fo]
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
    latest_reposts_list_ro = Repost.objects.filter(reposter_id=profile_id)
    latest_reposts_list = [get_object_or_404(Post, id=repost.post_id) for repost in latest_reposts_list_ro]
    context = {"latest_reposts_list": latest_reposts_list}
    return render(request, "posts.html", context)


@login_required
def view_user_likes(request, profile_id):
    latest_likes_list_lo = Like.objects.filter(liker_id=profile_id)
    latest_likes_list = [get_object_or_404(Post, id=like.post_id) for like in latest_likes_list_lo]
    context = {"latest_likes_list": latest_likes_list}
    return render(request, "posts.html", context)


@login_required
def view_user_bookmarks(request):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)
    latest_bookmarks_list_bo = Bookmark.objects.filter(bookmarker_id=requester.id)
    latest_bookmarks_list = [get_object_or_404(Post, id=bookmark.post_id) for bookmark in latest_bookmarks_list_bo]
    context = {"latest_bookmarks_list": latest_bookmarks_list}
    return render(request, "posts.html", context)


@login_required
def create_follow(request, profile_id):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    if requester.id == profile_id:
        return HttpResponseRedirect(reverse("profile:home", args=(profile_id,)))
    else:
        # check if they're already being followed 
        status = Follow.objects.filter(follower_id=profile_id, following_id=requester.id)

        # if they are make it mutual
        if status.exists():
            status[0].mutual=True
            status.save()
        # else create new follow record
        else:
            status = Follow(
                follower=requester,
                following_id=profile_id,
            )
            status.save()
        
        return HttpResponse()


@login_required
def delete_follow(request, profile_id):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    if requester.id == profile_id:
        return HttpResponseRedirect(reverse('profile:home'), args=(profile_id,))
    else:
        # check if requester was followed first
        status = Follow.objects.filter(follower_id=profile_id, following_id=requester.id)

        # if they were, unmutual the follow
        if status.exists():
            status[0].mutual=False
            status.save()
        else:
            # check if requester followed first
            status = Follow.objects.filter(follower_id=requester.id, following_id=profile_id)
            if status.exists():
                # if they were followed back, delete old record, create new Follow record with reversed roles
                if status[0].mutual:
                    status[0].delete()
                    status = Follow(
                        follower_id=profile_id,
                        following=requester,
                    )
                    status.save()
                # if they were never followed back just delete the record
                else:
                    status[0].delete()
            else:
                # Error if we get here, redirect to profile
                return HttpResponseRedirect(reverse("profile:home", args=(profile_id,)))
    
        return HttpResponse()


@login_required
def remove_follow(request, profile_id):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    if requester.id == profile_id:
        return HttpResponseRedirect(reverse('profile:home'), args=(profile_id,))
    else:
        # check if requester was followed first
        status = Follow.objects.filter(follower_id=profile_id, following_id=requester.id)

        if status.exists():
            status[0].delete()
        else:
            # check if requester followed first
            status = Follow.objects.filter(follower_id=requester.id, following_id=profile_id)
            if status.exists():
                status[0].delete()
            else:
                # Error if we get here, redirect to profile
                return HttpResponseRedirect(reverse("profile:home", args=(profile_id,)))
        
        return HttpResponse()


# def view_user_dp(request, profile_id):
#     user = get_object_or_404(UserProfile, id=user_id)
#     return render(request, "display_picture.html", {"image": user.display_picture})


# def user_media(request, profile_id):
#     pass

    

