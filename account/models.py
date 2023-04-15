from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


UserModel = get_user_model()
