
from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),  # Home page (all posts)
    path("index", views.index, name="index"),  

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("new", views.new_post, name="new_post"),  # New post
    path("posts", views.index, name="posts"),  

    path("profile/<str:username>", views.profile, name="profile"),  # User profile
    path("follow/<str:username>", views.follow_toggle, name="follow_toggle"),  # Follow/unfollow

    path("following", views.following, name="following"),  # Only posts by followed users

    path("edit/<int:post_id>", views.edit_post, name="edit_post"),  # Edit post
    path("like/<int:post_id>", views.like_post, name="like_post"),  # Like/unlike post
]
