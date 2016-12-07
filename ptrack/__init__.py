from django.views.generic import TemplateView
from django.shortcuts import HttpResponse
from django.conf import settings
import abc
from django.utils.module_loading import autodiscover_modules
from ptrack.trackers import tracker

default_app_config = 'ptrack.apps.PtrackConfig'

if not hasattr(settings,'PTRACK_SECRET'):
    raise Exception('PTRACK_SECRET is not defined')
elif len(settings.PTRACK_SECRET) > 32:
    raise Exception('PTRACK_SECRET must be less than 32 bytes')

def autodiscover():
    autodiscover_modules('pixels', register_to=tracker)

class TrackingPixel(object):
    '''
        The custom tracking pixel to be registered by client app.

        Callbacks:
        - record(): methods are executed when the tracking pixel loads
    '''
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def record(self, *args, **kwargs):
        raise NotImplementedError("record method has not been implemented")
