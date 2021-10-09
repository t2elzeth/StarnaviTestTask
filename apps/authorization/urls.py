from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("users", views.UsersViewSet)
router.register("token", views.TokenViewSet, basename="token-auth")

urlpatterns = router.urls
