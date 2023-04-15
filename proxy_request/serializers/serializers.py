import requests
from django.conf import settings
from django.utils.timezone import now
from rest_framework import serializers

from account.serializers.user_serializers import PublicUserSerializer
from proxy_request.models import LogRequest
from utils.serializers import redirect_url_validators


class SendRequestSerializer(serializers.Serializer):
    json = serializers.JSONField(default=None)
    headers = serializers.DictField(default=dict)
    url = serializers.CharField(required=True, validators=[redirect_url_validators])
    method = serializers.ChoiceField(
        choices=('GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE')
    )

    def get_files(self):
        files_start_with = 'files_'
        files_keys = [element for element in self.initial_data if element.startswith(files_start_with)]

        files_data = {f"{files_start_with}".join(element.split(f'{files_start_with}')[1:]): self.initial_data[element]
                      for element in files_keys}

        return files_data

    @staticmethod
    def formatted_headers(headers):
        results = {**headers}
        for key in results:
            if key in settings.LOG_SKIPPED_HEADERS:
                results[key] = ""
        return results

    def create(self, validated_data):
        files_data = self.get_files()
        user = self.context.get('request').user
        headers = {
            **validated_data['headers'],
            'Authorization': f'Bearer {settings.SHARED_KEY}'
        }

        payload = {
            "method": validated_data['method'],
            "json": validated_data['json'],
            "headers": headers,
            "url": validated_data['url'],
            "files": files_data
        }
        start_at = now()
        response = {}
        status_code = -1
        exception_message = None
        full_headers = {}
        try:
            req = requests.request(
                **payload
            )
        except Exception as e:
            exception_message = str(e)
        else:
            status_code = req.status_code
            full_headers = self.formatted_headers(req.request.headers)
            response['headers'] = {**req.headers}
            try:
                response['content'] = req.json()
            except requests.exceptions.JSONDecodeError:
                response['content'] = req.text

        end_at = now()

        remap = {
            "json": "json_body"
        }
        remapped_data = {}
        for key in remap:
            remapped_data[remap[key]] = validated_data[key]
            del validated_data[key]

        log = {
            **validated_data,
            **remapped_data,
            "start_at": start_at,
            "end_at": end_at,
            "sent_headers": full_headers,
            "status_code": status_code,
            "response": response,
            "exception_message": exception_message,
            "user": user
        }
        return LogRequest.objects.create(**log)

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        return LogRequestSerializer().to_representation(instance)


class LogRequestSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer()

    class Meta:
        model = LogRequest
        fields = '__all__'
