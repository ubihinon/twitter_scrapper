from rest_framework import views
from rest_framework.response import Response

from apps.common.serializers import TweetSerializer

PAGE_LIMIT = 30


class TweetListView(views.APIView):
    def get(self, request, **kwargs):
        limit = kwargs.get('limit', PAGE_LIMIT)
        print(f'Limit: {limit}')

        return Response(TweetSerializer([], many=True).data)
