from django.urls import path, include

from rest_framework.routers import DefaultRouter

from proxy_request.views.views import RequestViewSet, LogRequestViewSet, StatsViewSet

router = DefaultRouter()
router.register(r'call', RequestViewSet, basename='call')
router.register(r'logs', LogRequestViewSet, basename='log')
router.register(r'stats', StatsViewSet, basename='stats')


# registration

urlpatterns = [
    path('', include(router.urls))
]
