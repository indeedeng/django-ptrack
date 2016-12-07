from django.views.generic import TemplateView
from django.shortcuts import HttpResponse
from ptrack import tracker
from ptrack.utils import decrypt

TRANSPARENT_1_PIXEL_GIF = "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"

class TrackingPixel(TemplateView):
    
    def get(self, request, *args, **kwargs):
        ptrack_encrypted_data = kwargs['ptrack_encrypted_data']
        try:
            args, kwargs = decrypt(ptrack_encrypted_data)
            tracker.call_callbacks(*args, **kwargs)
        except TypeError, ValueError:
            # Ignore any non valid inputs
            pass
        return HttpResponse(TRANSPARENT_1_PIXEL_GIF, content_type='image/gif')

