from django.conf import settings
from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from proxy_request.models import LogRequest
from proxy_request.permissions.request_permissions import RequestPermission
from proxy_request.serializers.serializers import SendRequestSerializer, LogRequestSerializer
from proxy_request.utils import get_user_quota
from utils.pagination import StandardResultsSetPagination


class RequestViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = SendRequestSerializer
    permission_classes = (IsAuthenticated, RequestPermission)
    parser_classes = [
        JSONParser,
        MultiPartParser
    ]


class LogRequestViewSet(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = LogRequestSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('url', 'user__username', 'user__email', 'start_at', 'end_at')

    def get_queryset(self):
        queryset = LogRequest.objects.all()
        return queryset.order_by("-start_at")

    @action(detail=False, url_path='all', methods=('get',))
    def get_all(self, request):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(instance=filtered_queryset, many=True)
        return Response(data=serializer.data)


class StatsViewSet(GenericViewSet):

    @action(detail=False, url_path='quota', methods=('get',))
    def get_quota(self, request):
        count = get_user_quota(request.user)
        return Response(data={"current": count, "mex": settings.QUOTA_GLOBAL_MAX_REQUEST_COUNT})
