from django.urls import path

from .views import TweetListView

urlpatterns = [
    path('<slug:tag>/', TweetListView.as_view(), name='hashtags-tweets')
]
