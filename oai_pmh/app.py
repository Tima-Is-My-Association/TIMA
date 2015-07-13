from django.apps import AppConfig

class OAIPMHConfig(AppConfig):
    name = 'oai_pmh'
    verbose_name = 'OAI-PMH'

    def ready(self):
        import oai_pmh.signals
