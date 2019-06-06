from django.urls import path

from .views import UserTweetListView

urlpatterns = [
    path('<username>', UserTweetListView.as_view(), name='user-tweets')
]
