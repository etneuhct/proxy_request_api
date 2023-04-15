from django.conf import settings
from rest_framework import permissions

from proxy_request.utils import get_user_quota
from utils.error_messages import ErrorMessage


class RequestPermission(permissions.BasePermission):
    message = ErrorMessage.quota_exceeded

    def has_permission(self, request, view):
        user = request.user
        count = get_user_quota(user)
        return count < settings.QUOTA_GLOBAL_MAX_REQUEST_COUNT
