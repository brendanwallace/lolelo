from django.apps import AppConfig


class NaLcsConfig(AppConfig):
    name = 'nalcs'

    def ready(self):
        from nalcs import signals
