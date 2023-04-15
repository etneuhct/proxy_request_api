from django.conf import settings
from rest_framework import serializers

from utils.error_messages import ErrorMessage


class NullableCurrentUserDefault:
    requires_context = True

    def __call__(self, serializer_field):
        try:
            return serializer_field.context['request'].user
        except KeyError:
            return


class GenericCreationBaseSerializer(metaclass=serializers.SerializerMetaclass):
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), allow_null=True
    )


def redirect_url_validators(value: str):
    for url in settings.ALLOWED_REQUEST_URL:
        if url.startswith(value):
            return
    raise serializers.ValidationError(ErrorMessage.invalid_request_url)
