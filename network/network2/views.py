from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from .models import Post, User, Follow

User = get_user_model()

from .models import Follow, User, Post

def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network2/index.html", {
        "page_obj": page_obj,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network2/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network2/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network2/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network2/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network2/register.html")



@login_required
def like_post(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    post = get_object_or_404(Post, pk=post_id)

    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes": post.likes.count()
    })


@login_required
def edit_post(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        content = data.get("content", "")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)

        if request.user != post.author:
            return JsonResponse({"error": "You can only edit your own posts."}, status=403)

        post.content = content
        post.save()
        return JsonResponse({"message": "Post updated successfully."})
    return JsonResponse({"error": "PUT request required."}, status=400)


@login_required
def follow_toggle(request, username):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    to_follow = get_object_or_404(User, username=username)

    if to_follow == request.user:
        return JsonResponse({"error": "You cannot follow yourself."}, status=400)

    user = request.user

    follow_relation = Follow.objects.filter(follower=user, following=to_follow)

    if follow_relation.exists():
        # Unfollow
        follow_relation.delete()
        message = "Unfollowed"
    else:
        # Follow
        Follow.objects.create(follower=user, following=to_follow)
        message = "Followed"

    # Update followers count
    followers_count = Follow.objects.filter(following=to_follow).count()

    return JsonResponse({
        "message": message,
        "followers_count": followers_count
    })


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    posts = Post.objects.filter(author=profile_user).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()

    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    return render(request, "network2/profile.html", {
        "profile_user": profile_user,
        "page_obj": page_obj,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following
    })


@login_required
def following(request):
    # Get users that the logged-in user follows
    followed_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)

    posts = Post.objects.filter(author__in=followed_users).order_by('-timestamp')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network2/following.html", {
        "page_obj": page_obj
    })



@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            Post.objects.create(author=request.user, content=content)
        return HttpResponseRedirect(reverse("index"))
