""" Ptrack Django Views """
from django.views.generic import TemplateView
from django.shortcuts import HttpResponse
from ptrack import tracker
import ptrack

TRANSPARENT_1_PIXEL_GIF = "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"

class TrackingPixel(TemplateView):
    """ Calls tracker callback (record) and returns Tracking Pixel gif """

    def get(self, request, *args, **kwargs):
        """
        Record and return Tracking Pixel
        Only TrackingPixel method - POST, etc. are not supported
        """
        ptrack_encoded_data = kwargs['ptrack_encoded_data']

        args, kwargs = None, None
        try:
            args, kwargs = ptrack.ptrack_encoder.decrypt(ptrack_encoded_data)
        except (TypeError, ValueError):
            # Ignore any non valid inputs, which cannot be decrypted or deserialized
            pass

        if args or kwargs:
            tracker.call_callbacks(request, *args, **kwargs)
        return HttpResponse(TRANSPARENT_1_PIXEL_GIF, content_type='image/gif')
