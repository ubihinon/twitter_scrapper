from django.urls import path

from .views import TweetListByHashtagView

urlpatterns = [
    path('<hashtag>', TweetListByHashtagView.as_view(), name='hashtags-tweets')
]
