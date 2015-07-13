from django.apps import AppConfig

class ApplicationConfig(AppConfig):
    name = 'applications'

    def ready(self):
        import applications.signals
