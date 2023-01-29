"""Ptrack Setup"""
import abc
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import autodiscover_modules

from ptrack.encoder import PtrackEncoder
from ptrack.trackers import tracker

default_app_config = 'ptrack.apps.PtrackConfig'
ptrack_encoder = PtrackEncoder

if not hasattr(settings, 'PTRACK_SECRET'):
    raise ImproperlyConfigured('PTRACK_SECRET is not defined')
elif len(settings.PTRACK_SECRET) > 32:
    raise ImproperlyConfigured('PTRACK_SECRET must be less than 32 bytes')



def autodiscover():
    """
    Autodiscover pixels.py file in project directory,
    then register tracker.
    """
    autodiscover_modules('pixels', register_to=tracker)


class TrackingPixel(object):
    """The custom tracking pixel registered by tracker."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def record(self, *args, **kwargs):
        """Callback executed when the tracking pixel img loads."""
        raise NotImplementedError("record method has not been implemented")
