from django.apps import AppConfig


class ProxyRequestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'proxy_request'

    def ready(self):
        from proxy_request.signals import init_signals
        init_signals()
        return super(ProxyRequestConfig, self).ready()