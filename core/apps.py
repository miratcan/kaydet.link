# pylint: disable=W0611,C0415
# ruff: noqa: F401,PLC0415
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .signals import bookmark_signals, comment_signals, link_signals
