"""Ptrack Django URL Configuration."""
from django.urls import re_path

from ptrack.views import TrackingPixel

urlpatterns = [
    re_path(r"^(?P<ptrack_encoded_data>.{132}?)/$", TrackingPixel.as_view(), name="ptrack"),
]
