from django.views.generic import TemplateView
from django.shortcuts import HttpResponse
import abc


class TrackingPixelBase(TemplateView):
    __metaclass__ = abc.ABCMeta
    def get(self, request, *args, **kwargs):
        ptrack_encrypted_data = kwargs['ptrack_encrypted_data']
        
        TRANSPARENT_1_PIXEL_GIF = "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
        return HttpResponse(TRANSPARENT_1_PIXEL_GIF, content_type='image/gif')

    @abc.abstractmethod
    def record(self, *args, **kwargs):
        raise NotImplementedError("record method has not been implemented")


TRACKING_PIXEL_REGISTRY = None 
def register(instance):
    global TRACKING_PIXEL_REGISTRY
    '''
    Global record keeping of 
    '''
    if isinstance(instance, TrackingPixelBase):
        if TRACKING_PIXEL_REGISTRY:
            raise Exception("ptrack already has an instance of TrackPixelBase registered")
        else:
            TRACKING_PIXEL_REGISTRY = instance
    raise Exception(instance + "is not an instance of TrackingPixelBase")
