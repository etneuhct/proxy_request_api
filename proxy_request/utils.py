from django.conf import settings

from proxy_request.constants import QuotaMode
from proxy_request.models import LogRequest


def get_user_quota(user):
    quota_mode = QuotaMode.count_per_user
    count = 0
    if quota_mode == QuotaMode.count_per_user or quota_mode == QuotaMode.count_global:
        queryset = LogRequest.objects.filter()
        if quota_mode == QuotaMode.count_per_user:
            queryset = LogRequest.objects.filter(
                user=user,
            )
        if settings.QUOTA_EXCLUDED_STATUS_CODE:
            queryset = queryset.exclude(status_code__in=settings.QUOTA_EXCLUDED_STATUS_CODE)

        if settings.QUOTA_INCLUDED_STATUS_CODE:
            queryset = queryset.filter(status_code__in=settings.QUOTA_INCLUDED_STATUS_CODE)

        if settings.QUOTA_EXCLUDED_INCOMPLETE_REQUEST:
            queryset = queryset.filter(exception_message__isnull=True)
        count = queryset.count()
    return count
