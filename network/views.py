from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core import serializers
from datetime import datetime



from .models import Post, User


def index(request):
    posts = Post.objects.all().order_by('-date')
    paginator = Paginator(posts, 10) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', {'page_obj': page_obj})

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def new_post(request):
    if request.method == "POST":
        post = request.POST.get('post')
        user = User.objects.get(username=request.user.username)
        add_post = Post(post=post, user=user, date=datetime.now())
        add_post.save()
        return redirect('/')

    return render(request, 'network/new_post.html')


def profile(request, userid):
    profile = User.objects.get(username=userid)
    status = int(User.objects.get(username=request.user.username) in profile.followers.all())

    print(profile.username, User.objects.get(username=request.user.username), status)
    print(f'Following {profile.followings.all()}')
    print(f'Followers {profile.followers.all()}')
    posts = Post.objects.filter(user=profile).order_by('-date')
    paginator = Paginator(posts, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/profile.html', {'profile':profile, 'posts':page_obj, 'following':len(profile.followings.all()), 'follower':len(profile.followers.all()), 'status':status})


@login_required
def follow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    print(data, request.user.username)

    target_user = User.objects.get(username=request.user.username)
    other_user = User.objects.get(username=data['following'])

    if data['status'] == '1':
        target_user.followings.remove(other_user)
        other_user.followers.remove(target_user)

    elif data['status'] == '0':
        target_user.followings.add(other_user)
        other_user.followers.add(target_user)


    print(target_user.followings.all())
    print(other_user.followers.all())


    return JsonResponse({"followers": len(other_user.followers.all())}, status=200)

@login_required
def followings(request):
    following = User.objects.get(username=request.user.username).followings.all()
    # print(Post.objects.filter(user=))
    posts = []
    print(following)
    for _ in following:
        posts.extend(Post.objects.filter(user=_))
    # posts = Post.objects.all().order_by('-date').exclude(user=request.user)
    paginator = Paginator(posts, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/index.html', {'page_obj': page_obj})

@login_required
def edit_post(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    if Post.objects.get(id=id).user == request.user:
        Post.objects.filter(id=id).update(post=data['data'], date=datetime.now())
        print(data, request.user.username)
        post = Post.objects.get(id=id)
        return JsonResponse({'post':post.serialize()}, status=200)
    else:
        return JsonResponse({"error": "You cant edit others tweet"}, status=200)


@login_required
def likes(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    print(id)

    if id == 'undefined':
        return JsonResponse({"error": "Something went wrong!"}, status=200)

    likes = Post.objects.get(id=id).liked

    if not request.user in likes.all():
        likes.add(request.user)
    else:
        likes.remove(request.user)


    return JsonResponse({"likes": len(likes.all())}, status=200)