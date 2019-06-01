from django.urls import path

from .views import TweetListByHashtagView

urlpatterns = [
    path('<tag>', TweetListByHashtagView.as_view(), name='hashtags-tweets')
]
