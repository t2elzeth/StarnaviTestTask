from django.urls import path
from rest_framework import routers

from .views import LikeUnlikeViewSet, PostAnalytics, PostCreateAPIView

router = routers.DefaultRouter()
router.register("", LikeUnlikeViewSet, basename="post-rate")

urlpatterns = [
    path("create/", PostCreateAPIView.as_view(), name="post_create"),
    path("analytics/<int:pk>/", PostAnalytics.as_view(), name="post_analytics"),
]

urlpatterns += router.urls
