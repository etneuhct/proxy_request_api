from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.views.login_views import LoginViewSet

router = DefaultRouter()
router.register(r'login', LoginViewSet, basename='login', )

# registration

urlpatterns = [
    path('', include(router.urls))
]
