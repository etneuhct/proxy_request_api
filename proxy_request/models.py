from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class LogRequest(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT)

    url = models.CharField(max_length=256)
    method = models.CharField(max_length=8)
    json_body = models.JSONField(default=dict, null=True)
    headers = models.JSONField(default=dict)

    sent_headers = models.JSONField(default=dict)
    response = models.JSONField(default=dict)
    status_code = models.IntegerField(default=-1)
    exception_message = models.TextField(default=None, null=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
