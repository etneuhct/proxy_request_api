from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from account.models import UserModel
from utils.error_messages import ErrorMessage
from utils.exceptions import ForbiddenRequestException



class UserTokenSerializer(serializers.Serializer):

    def to_representation(self, instance):
        token = AccessToken.for_user(instance)
        refresh_token = RefreshToken.for_user(instance)
        return {
            "access_token": str(token),
            "refresh_token": str(refresh_token)
        }


class RefreshSerializer(UserTokenSerializer):
    refresh_token = serializers.CharField()

    def create(self, validated_data):
        refresh = RefreshToken(validated_data["refresh_token"])
        user_id = refresh['user_id']
        user = UserModel.objects.get(id=user_id)
        return user


class LoginSerializer(UserTokenSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    @staticmethod
    def create(validated_data):
        email = validated_data['email']
        password = validated_data['password']
        try:
            user = UserModel.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            raise ForbiddenRequestException(ErrorMessage.username_password_mismatch)
        if not user.check_password(password):
            raise ForbiddenRequestException(ErrorMessage.username_password_mismatch)
        return user
