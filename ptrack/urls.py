from django.conf.urls import patterns, url
from . import TRACKING_PIXEL_REGISTRY


urlpatterns = patterns('',
    url(r'^(?P<ptrack_encrypted_data>.*?)', TRACKING_PIXEL_REGISTRY.as_view(), name="ptrack"),
)