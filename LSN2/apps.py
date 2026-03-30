from django.apps import AppConfig, apps

class Lsn2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LSN2'

    def ready(self):
        from .models import Profile  # safe import here
        if not apps.is_installed('some_other_app'):
            print("Some other app is not installed!")