from django.conf.urls import patterns, url
from ptrack.views import TrackingPixel


urlpatterns = patterns('',
    url(r'^(?P<ptrack_encrypted_data>.*?)/$', TrackingPixel.as_view(), name="ptrack"),
)