"""twitter_scrapper URL Configuration

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
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view


swagger_view = get_swagger_view(title='TwitterScrapper API')

API_ENDPOINTS = [
    path('hashtags/', include('apps.hashtags.urls')),
    path('users/', include('apps.users.urls'))
]

urlpatterns = [
    path('docs', swagger_view),
    path('', include(API_ENDPOINTS)),
]
