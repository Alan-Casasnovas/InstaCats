"""
URL configuration for varnaWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
    path("photo_list/", views.photo_list, name="photo_list"),
    path("photo/<int:pk>/", views.photo_detail, name="photo_detail"),
    path("add/", views.add_photo, name="add_photo"),
    path("delete/<int:pk>/", views.delete_photo, name="delete_photo"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
