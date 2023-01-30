"""AppConfig Setup."""
from django.apps import AppConfig


class SimplePtrackConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = "ptrack"
    default = False

    def ready(self):
        """Appconfig no operation on ready."""
        super().ready()


class PtrackConfig(SimplePtrackConfig):
    """The default AppConfig for ptrack which does autodiscovery."""

    default = True

    def ready(self):
        """Appconfig execute autodiscover on ready."""
        super().ready()
        self.module.autodiscover()
