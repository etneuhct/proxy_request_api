from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Create admin'

    def handle(self, *args, **options):
        username = settings.DEFAULT_ADMIN_USERNAME
        email = settings.DEFAULT_ADMIN_EMAIL
        password = settings.DEFAULT_ADMIN_PASSWORD
        User.objects.update_or_create(
            username=username,
            email=email,
            defaults={'password': make_password(password),
                      'is_staff': True, 'is_superuser': True})
