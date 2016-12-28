from django.conf.urls import patterns, url
from ptrack.views import TrackingPixel


urlpatterns = patterns('',
    url(r'^(?P<ptrack_encoded_data>.*?)/$', TrackingPixel.as_view(), name="ptrack"),
)