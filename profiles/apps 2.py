from django.apps import AppConfig
import uuid 


# ProfilesConfig.default_auto_field -> primary key
class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        from . import signals

