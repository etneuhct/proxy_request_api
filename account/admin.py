from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import UserModel


class CustomAdmin(UserAdmin):
    pass


admin.site.register(UserModel, CustomAdmin)
