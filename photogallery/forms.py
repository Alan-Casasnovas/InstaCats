from django import forms
from .models import Photo, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "description"]
        app_label = "photogallery"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
