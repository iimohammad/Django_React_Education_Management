import os

from django.apps import AppConfig
from django.conf import settings

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)