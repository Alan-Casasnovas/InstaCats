from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Photo, Comment
from .forms import SignupForm, LoginForm, PhotoForm, CommentForm


def home(request):
    return render(request, "home.html")


def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")


def photo_list(request):
    photos = Photo.objects.all()
    hashtag = request.GET.get("hashtag")
    if hashtag:
        photos = photos.filter(Q(description__icontains=f"#{hashtag}"))
    return render(request, "photo_list.html", {"photos": photos})


def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    comments = Comment.objects.filter(photo=photo)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.photo = photo
            comment.save()
            return redirect("photo_detail", pk=pk)
    else:
        form = CommentForm()
    return render(
        request,
        "photo_detail.html",
        {"photo": photo, "comments": comments, "form": form},
    )


@login_required
def add_photo(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect("photo_detail", pk=photo.pk)
    else:
        form = PhotoForm()
    return render(request, "add_photo.html", {"form": form})


@login_required
def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if photo.user == request.user:
        photo.delete()
    return redirect("photo_list")
