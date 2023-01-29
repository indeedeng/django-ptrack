""" Ptrack Django Views """
from base64 import b64decode

from django.shortcuts import HttpResponse
from django.views.generic import TemplateView

import ptrack
from ptrack import tracker
from nacl.exceptions import CryptoError

TRANSPARENT_1_PIXEL_PNG = b64decode(
    b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)
TRANSPARENT_1_PIXEL_GIF = b64decode(
    b"R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
)


class TrackingPixel(TemplateView):
    """Calls tracker callback (record) and returns Tracking Pixel gif"""

    def get(self, request, *args, **kwargs):
        """
        Record and return Tracking Pixel
        Only TrackingPixel method - POST, etc. are not supported
        """
        ptrack_encoded_data = kwargs["ptrack_encoded_data"]

        args, kwargs = (), {}
        try:
            args, kwargs = ptrack.ptrack_encoder.decrypt(ptrack_encoded_data)
        except (TypeError, ValueError, CryptoError):
            # Ignore any non valid inputs, which cannot be decrypted or deserialized
            pass

        if args or kwargs:
            tracker.call_callbacks(request, *args, **kwargs)
        # return HttpResponse(TRANSPARENT_1_PIXEL_GIF, content_type='image/gif')
        return HttpResponse(TRANSPARENT_1_PIXEL_PNG, content_type="image/png")
