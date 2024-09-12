from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse 

from homepage.views import create_combined_posts, create_post_in_post_object
from posts.models import Comment
from posts.models import Post
from posts.models import Quote    
from users.models import CustomUser
from user_profile.models import UserProfile

from .templates.forms.comment_form import NewCommentForm
from .templates.forms.post_form import NewPostForm

@login_required
def display_post(request, post_id, post_op_id):
    post = get_object_or_404(Post, id=post_id)
    
    # get comments, filter out op comments from others
    latest_comments_raw = post.comments.all()
    latest_comments_op = latest_comments_raw.filter(poster_id=post_op_id)
    latest_comments_all = latest_comments_raw.exclude(poster_id=post_op_id)

    og_post_info = create_combined_posts([post])
    op_post_comments = create_combined_posts(latest_comments_op)
    latest_comments = create_combined_posts(latest_comments_all)

    context = {'og_post':og_post_info, 'op_comments':op_post_comments, 'latest_comments_list':latest_comments}

    return render(request, "display_post.html", context)

@login_required
def create_like(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    if og_post.likes.contains(requester):
        delete_like(request=request, post_id=post_id)
    else:
        og_post.likes.add(requester)

    return HttpResponse(status=200, content=og_post.getLikes())

@login_required
def delete_like(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)
    post_liker_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    post_liker = get_object_or_404(UserProfile, user_id=post_liker_cu.id)
    og_post.likes.remove(post_liker)
    return HttpResponse(status=200)

@login_required
def create_repost(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    if og_post.reposts.contains(requester):
        delete_repost(request=request, post_id=post_id)
    else:
        og_post.reposts.add(requester)

    return HttpResponse(status=200, content=og_post.getReposts())

@login_required
def delete_repost(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)
    post_reposter_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    post_reposter = get_object_or_404(UserProfile, user_id=post_reposter_cu.id)
    og_post.reposts.remove(post_reposter)
    return HttpResponse(status=200)

@login_required
def create_bookmark(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)
    requester_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    requester = get_object_or_404(UserProfile, user_id=requester_cu.id)

    if og_post.bookmarks.contains(requester):
        delete_bookmark(request=request, post_id=post_id)
    else:
        og_post.bookmarks.add(requester)

    return HttpResponse(status=200, content=og_post.getBookmarks())

@login_required
def delete_bookmark(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)
    post_bookmarker_cu = get_object_or_404(CustomUser, email=request.user.get_username())
    post_bookmarker = get_object_or_404(UserProfile, user_id=post_bookmarker_cu.id)
    og_post.bookmarks.remove(post_bookmarker) 
    return HttpResponse(status=200)

@login_required
def get_comments_count(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)
    return HttpResponse(status=200, content=og_post.getComments())

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
                body = form.cleaned_data["body"]
            )

            new_post.save()
            og_post.quotes.add(new_post)
            og_post.save()

            return HttpResponse(status=204)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewPostForm()
        og_post_stripped = {
            "body":og_post.body,
        }

    return render(request, "new_quote.html", {"form": form, "og_post": og_post_stripped})

@login_required
def delete_quote(request, post_id):
    quote = get_object_or_404(Quote, id=post_id)
    og_poster_up = get_object_or_404(UserProfile, id=quote.poster_id)
    og_poster = get_object_or_404(CustomUser, id=og_poster_up.user_id)

    if request.user.get_username() == og_poster.get_username():   
        quote.delete()
        return redirect(request.META.get('HTTP_REFERER', 'home/'))
    else:
        return redirect(reverse('homepage:home')) # change this to homepage once you have a homepage

@login_required
def create_comment(request, post_id):
    og_post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NewCommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            poster_cu = get_object_or_404(CustomUser, email=request.user.get_username())
            poster = get_object_or_404(UserProfile, user_id=poster_cu.id)

            new_post = Comment(
                reply_post = og_post,
                poster = poster,
                body = form.cleaned_data["body"]
            )

            new_post.save()
            og_post.comments.add(new_post)
            og_post.save()

            return HttpResponse(status=204)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewCommentForm()
        og_post_stripped = create_post_in_post_object(og_post)

    return render(request, "new_comment.html", {"form": form, "og_post": og_post_stripped,})

@login_required
def delete_comment(request, post_id):
    comment = get_object_or_404(Comment, id=post_id)
    og_poster_up = get_object_or_404(UserProfile, id=comment.poster_id)
    og_poster = get_object_or_404(CustomUser, id=og_poster_up.user_id)

    if request.user.get_username() == og_poster.get_username():   
        comment.delete()
        return redirect(reverse('homepage:home'))
    else:
        return redirect(reverse('homepage:home')) # homepage


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
                body = form.cleaned_data["body"]
            )

            new_post.save()
            return HttpResponse(status=204)

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
        return redirect(reverse('homepage:home'))
    else:
        return redirect(reverse('homepage:home')) # homepage
    


