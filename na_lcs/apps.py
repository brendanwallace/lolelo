from django.apps import AppConfig


class NaLcsConfig(AppConfig):
    name = 'na_lcs'

    def ready(self):
        from na_lcs import signals
