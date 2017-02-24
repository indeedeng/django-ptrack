""" Ptrack Django URL Configuration """
from django.conf.urls import url
from ptrack.views import TrackingPixel


urlpatterns = [
    url(r'^(?P<ptrack_encoded_data>.*?)/$', TrackingPixel.as_view(), name="ptrack"),
]
