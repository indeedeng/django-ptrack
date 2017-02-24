"""AppConfig Setup"""
from django.apps import AppConfig

class SimplePtrackConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = 'ptrack'

    def ready(self):
        super(SimplePtrackConfig, self).ready()

class PtrackConfig(SimplePtrackConfig):
    """The default AppConfig for ptrack which does autodiscovery."""

    def ready(self):
        super(PtrackConfig, self).ready()
        self.module.autodiscover()
