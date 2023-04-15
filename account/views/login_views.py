from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account.serializers.login_serializers import RefreshSerializer, LoginSerializer


class LoginViewSet(GenericViewSet):
    permission_classes = []
    authentication_classes = []
    serializer_class = LoginSerializer

    def get_serializer_class(self):
        serializer_mapping = {
            'refresh': RefreshSerializer,
        }
        try:
            return serializer_mapping[self.action]
        except KeyError:
            return super(LoginViewSet, self).get_serializer_class()

    def create(self, request):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

    @action(detail=False, methods=('post',), url_path='refresh')
    def refresh(self, request):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
