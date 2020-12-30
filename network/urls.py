
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_post, name="new_post"),
    path("followings", views.followings, name="followings"),
    path(r"profile/<str:userid>/", views.profile, name="profile"),

    # API routes
    path('follow', views.follow, name="follow"),
    path(r'post/<int:id>', views.edit_post, name="edit_post"),
    path(r'likes/<int:id>', views.likes, name="likes"),
]
