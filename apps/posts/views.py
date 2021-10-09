from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filters import LikeAnalyticsFilterBackend
from .models import Like, Post
from .permissions import QueryParamsProvided
from .serializers import PostAnalyticsSerializer, PostSerializer


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class LikeUnlikeViewSet(GenericViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=True)
    def like(self, request, *args, **kwargs):
        Like.objects.create(liked_by=self.request.user, post=self.get_object())
        return Response(status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True)
    def unlike(self, request, *args, **kwargs):
        Like.objects.filter(liked_by=self.request.user, post=self.get_object()).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostAnalytics(generics.ListAPIView):
    serializer_class = PostAnalyticsSerializer
    permission_classes = [QueryParamsProvided]
    filter_backends = [LikeAnalyticsFilterBackend]

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs["pk"])

        return Like.objects.filter(post=post)

    def _get_likes_aggregated_by_day(self, list_of_likes):
        """
        The function returns the number of likes by day,
        where the key is the date and the value is the number of likes for that day.
        """
        likes_by_day = {}

        for like in list_of_likes:
            date_created = like["date_created"]
            likes = likes_by_day.get(date_created, 0)
            likes_by_day[date_created] = likes + 1
        return likes_by_day

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                "likes_overall": len(serializer.data),
                "by_day": self._get_likes_aggregated_by_day(serializer.data),
            }
        )
