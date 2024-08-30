import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse 
from django.utils import timezone

from homepage.models import PostTraction
from posts.models import Comment
from posts.models import Post
from posts.models import Quote    
from users.models import CustomUser
from user_profile.models import UserProfile

def create_combined_post(posts, users, cusers, comments, reposts, likes, bookmarks):
    combined_posts = []
    
    for post, profile, account, comments_count, reposts_count, likes_count, bookmarks_count in zip(posts, users, cusers,comments, reposts, likes, bookmarks):

        # Take only the data we need from post object
        post_stripped = {
            "id":post.id,
            "body":post.body,
            "pub_date":post.date_posted,
        }

        # Take only the data we need from user profile object
        profile_stripped = {
            "display_name":profile.display_name,
            # "display_picture":profile.display_picture,
        }

        account_stripped = {
            "username":account.user_name
        }

        combined_post = {
            "post":post_stripped, 
            "poster_profile":profile_stripped, 
            "poster_account":account_stripped,
            "comments_count":comments_count,
            "reposts_count":reposts_count,
            "likes_count":likes_count,
            "bookmarks_count":bookmarks_count,
        }
        combined_posts.append(combined_post)

    return combined_posts 

@login_required
def view_posts(request):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    # popular posts time delta
    pop_post_td = timezone.now() - datetime.timedelta(hours=48)

    # # most popular posts
    # latest_posts_pt = PostTraction.objects.filter(pub_date__gte=pop_post_td).order_by("-score")

    # # most popular friends posts
    # latest_friends_posts = PostTraction.objects.filter()

    # latest_posts = [get_object_or_404(Post, id=pt_post.post_id) for pt_post in latest_posts_pt]

    latest_posts = Post.objects.all()
    latest_posts_users = [get_object_or_404(UserProfile, id=p.poster_id) for p in latest_posts]
    latest_posts_cu = [get_object_or_404(CustomUser, id=u.user_id) for u in latest_posts_users]
    latest_posts_comments = [(p.comments.count()) for p in latest_posts] 
    latest_posts_reposts = [(p.reposts.count() + p.quotes.count()) for p in latest_posts] 
    latest_posts_likes = [(p.likes.count()) for p in latest_posts]
    latest_posts_bookmarks = [(p.bookmarks.count()) for p in latest_posts]

    posts = create_combined_post(latest_posts, latest_posts_users, latest_posts_cu, latest_posts_comments, latest_posts_reposts, latest_posts_likes, latest_posts_bookmarks)

    
    context = {"latest_posts_list": posts,}
    return render(request, "homepage.html", context)

@login_required
def search(request):
    pass

