from django.apps import AppConfig

MODULE_NAME = 'coremis_app_integration'

DEFAULT_CONFIG = {}


class CoremisAppIntegrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = MODULE_NAME

    def ready(self):
        from core.models import ModuleConfiguration

        cfg = ModuleConfiguration.get_or_default(self.name, DEFAULT_CONFIG)
        self.__load_config(cfg)

    @classmethod
    def __load_config(cls, cfg):
        """
        Load all config fields that match current AppConfig class fields, all custom fields have to be loaded separately
        """
        for field in cfg:
            if hasattr(CoremisAppIntegrationConfig, field):
                setattr(CoremisAppIntegrationConfig, field, cfg[field])
