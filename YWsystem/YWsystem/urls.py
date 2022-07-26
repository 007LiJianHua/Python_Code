"""YWsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from app01 import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('register/', views.register),
    path('index/', views.index),
    re_path('showhost-(\d+)/', views.showhost, name="showhost"),
    re_path('^pushhost-(\d+)/$', views.push_showhost, name="push_showhost"),
    re_path('^jobhost-(\d+)/$', views.job_showhost, name="job_showhost"),
    path('addhost/', views.addhost),
    path('createhost/', views.createhost),
    path('hostdetail/', views.hostdetail),
    path('push/', views.push),
    path('job/', views.job),
    path('showapp/', views.showapp),
    re_path('^remove/*', views.remove),
]
