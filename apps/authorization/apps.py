import importlib

from django.apps import AppConfig


class AuthorizationConfig(AppConfig):
    name = "authorization"

    def ready(self):
        importlib.import_module(".signals", "authorization")
        return super().ready()
