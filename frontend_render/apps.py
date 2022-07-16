# pylint:disable=missing-class-docstring, missing-module-docstring
from django.apps import AppConfig


class FrontendRenderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'frontend_render'
