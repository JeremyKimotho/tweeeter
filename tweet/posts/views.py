from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse 

from posts.models import Comment
from posts.models import Post
from posts.models import Quote    
from users.models import CustomUser
from user_profile.models import UserProfile

from .templates.forms.post_form import NewPostForm

def display_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "display_post.html", {post: "post"})

@login_required
def create_like(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)
    post_liker_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    post_liker = get_object_or_404(UserProfile, user_id=post_liker_cu.id)
    og_post.likes.add(post_liker)   
    return HttpResponse()

@login_required
def delete_like(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)
    post_liker_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    post_liker = get_object_or_404(UserProfile, user_id=post_liker_cu.id)
    og_post.likes.remove(post_liker)
    return HttpResponse()

@login_required
def create_repost(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)
    post_reposter_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    post_reposter = get_object_or_404(UserProfile, user_id=post_reposter_cu.id)
    og_post.reposts.add(post_reposter)
    return HttpResponse()

@login_required
def delete_repost(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)
    post_reposter_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    post_reposter = get_object_or_404(UserProfile, user_id=post_reposter_cu.id)
    og_post.reposts.remove(post_reposter)
    return HttpResponse()

@login_required
def create_bookmark(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)
    post_bookmarker_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    post_bookmarker = get_object_or_404(UserProfile, user_id=post_bookmarker_cu.id)
    og_post.bookmarks.add(post_bookmarker) 
    return HttpResponse()

@login_required
def delete_bookmark(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)
    post_bookmarker_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    post_bookmarker = get_object_or_404(UserProfile, user_id=post_bookmarker_cu.id)
    og_post.bookmarks.remove(post_bookmarker) 
    return HttpResponse()

@login_required
def create_quote(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NewPostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            poster_cu = get_object_or_404(CustomUser, email=request.user.get_username())
            poster = get_object_or_404(UserProfile, user_id=poster_cu.id)

            new_post = Quote(
                quote_post = og_post,
                poster = poster,
                body = form.fields["body"]
            )

            new_post.save()
            return HttpResponse()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewPostForm()

    return render(request, "new_quote.html", {"form": form})

@login_required
def delete_quote(request, post_id):
    quote = get_object_or_404(Quote, id=post_id)
    og_poster_up = get_object_or_404(UserProfile, id=quote.poster_id)
    og_poster = get_object_or_404(CustomUser, id=og_poster_up.user_id)

    if request.user.get_username() == og_poster.get_username():   
        quote.delete()
        return HttpResponse()
    else:
        return HttpResponseRedirect(reverse('posts:create_post')) # change this to homepage once you have a homepage

@login_required
def create_comment(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NewPostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            poster_cu = get_object_or_404(CustomUser, email=request.user.get_username())
            poster = get_object_or_404(UserProfile, user_id=poster_cu.id)

            new_post = Comment(
                reply_post = og_post,
                poster = poster,
                body = form.fields["body"]
            )

            new_post.save()
            return HttpResponse()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewPostForm()

    return render(request, "new_comment.html", {"form": form})

@login_required
def delete_comment(request, post_id):
    comment = get_object_or_404(Comment, id=post_id)
    og_poster_up = get_object_or_404(UserProfile, id=comment.poster_id)
    og_poster = get_object_or_404(CustomUser, id=og_poster_up.user_id)

    if request.user.get_username() == og_poster.get_username():   
        comment.delete()
        return HttpResponse()
    else:
        return HttpResponseRedirect(reverse('homepage:home')) # homepage


@login_required
def create_post(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NewPostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            poster_cu = get_object_or_404(CustomUser, email=request.user.get_username())
            poster = get_object_or_404(UserProfile, user_id=poster_cu.id)

            new_post = Post(
                poster = poster,
                body = form.fields["body"]
            )

            new_post.save()
            return HttpResponse()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewPostForm()

    return render(request, "new_post.html", {"form": form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    og_poster_up = get_object_or_404(UserProfile, id=post.poster_id)
    og_poster = get_object_or_404(CustomUser, id=og_poster_up.user_id)

    if request.user.get_username() == og_poster.get_username():   
        post.delete()
        return HttpResponse()
    else:
        return HttpResponseRedirect(reverse('homepage:home')) # homepage

