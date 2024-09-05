"""This Django is for App Configuration"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """This is User App where the login, signin, home pages are handled"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
