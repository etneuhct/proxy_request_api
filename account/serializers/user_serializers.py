from rest_framework import serializers

from account.models import UserModel


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email')
