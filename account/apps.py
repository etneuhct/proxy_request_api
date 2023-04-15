from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        from account.signals import init_signals
        init_signals()
        return super(AccountConfig, self).ready()