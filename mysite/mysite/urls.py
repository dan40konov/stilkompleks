"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myarts/', include('myarts.urls')),
    path('pics/', include('pics.urls')),
    path('authz/', include('authz.urls')),
    path('users/', include('users.urls')),
    path('forums/', include('forums.urls')),
    path('dj_project/', include('dj_project.urls')),
    path('api/', include('api.urls')),
    path('api_example/', include('api_example.urls')),
    path('', include('home.urls')),  # Change to ads.urls
    path('accounts/', include('django.contrib.auth.urls')),  # Add
]
