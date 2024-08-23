import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse 
from django.utils import timezone

from homepage.models import PostTraction
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
def view_posts(request):
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    # popular posts time delta
    pop_post_td = timezone.now() - datetime.timedelta(hours=48)

    # most popular posts
    latest_posts_pt = PostTraction.objects.filter(pub_date__mte=pop_post_td).order_by("-score")

    # most popular friends posts
    latest_friends_posts = PostTraction.objects.filter()

    latest_posts = [get_object_or_404(Post, id=pt_post.post_id) for pt_post in latest_posts_pt]
    
    context = {"latest_posts_list": latest_posts}
    return render(request, "homepage.html", context)

