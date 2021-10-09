from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import TokenSerializer, UserActivitySerializer, UserSerializer


class UsersViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        if self.action == "my_activity":
            return self.request.user

    @action(methods=["post"], detail=False)
    def signup(self, request):
        return self.create(request)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated],
        serializer_class=UserActivitySerializer,
    )
    def my_activity(self, request):
        return self.retrieve(request)


class TokenViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = TokenSerializer

    @action(methods=["post"], detail=False)
    def login(self, request):
        return self.create(request)

    @action(methods=["post"], detail=False, permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.user.logout()
        return Response(status=status.HTTP_204_NO_CONTENT)
