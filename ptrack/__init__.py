"""Ptrack Setup."""
import abc

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import autodiscover_modules

from ptrack.encoder import PtrackEncoder
from ptrack.trackers import tracker

ptrack_encoder = PtrackEncoder

if not hasattr(settings, "PTRACK_SECRET"):
    raise ImproperlyConfigured("PTRACK_SECRET is not defined")
elif len(settings.PTRACK_SECRET) > 32:
    raise ImproperlyConfigured("PTRACK_SECRET must be less than 32 bytes")


def autodiscover():
    """Autodiscover pixels.py file in project directory and register tracker(s)."""
    autodiscover_modules("pixels", register_to=tracker)


class TrackingPixel:
    """The custom tracking pixel registered by tracker."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def record(self, *args, **kwargs):
        """Execute callback when the tracking pixel image loads."""
        raise NotImplementedError("record method has not been implemented")
