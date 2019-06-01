from django.urls import path

from .views import UserTweetListView

urlpatterns = [
    path('<user>', UserTweetListView.as_view(), name='user-tweets')
]
