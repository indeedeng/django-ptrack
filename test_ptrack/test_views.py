"""Ptrack test views."""
import imghdr
import re
from tempfile import NamedTemporaryFile
from unittest.mock import MagicMock

from django.template import engines
from django.test import TestCase
from django.urls import reverse

import ptrack
from ptrack.views import TRANSPARENT_1_PIXEL_GIF

# setup
_test_data_params = [
    {"args": ["testarg"], "kwargs": {"testkey1": "testarg1", "testkey2": "testarg2"}},
    {
        "args": [
            "thisisalongtestarg1",
            "thisisalongtestarg2",
            "thisisalongtestarg3",
            "thisisalongtestarg4",
        ],
        "kwargs": {
            "thisisalongtestkey1": "thisisalongtestkwargvalue1",
            "thisisalongtestkey2": "thisisalongtestkwargvalue2",
        },
    },
    {"args": ["[][][][]]", "$%^&%%^$"], "kwargs": {"one": "[]][]]", "two": "[][][]]"}},
    {"args": ["testarg1", "testarg2", "testarg3"], "kwargs": {}},
    {"args": [], "kwargs": {"testkey1": "testarg1", "testkey2": "testarg2"}},
]
_test_encrypted_str = "Ylk67uIkGhy5_ugiHhAgu0_oG72_S-lSGGfHeZOUjJBJZwzNOYruvZqhnQAnGv93td1YvI5K_W-telcEya7vSEosk66TyW00i5lM2_iWAr995vLjyxaL9Z5qBsG3BRec11mS652MhV2x1whSC35VpP63J-WjEP1ejl8AW68cuduH8HdfQSC6draXF7BWuiha706NYnXtESJDACsBJaUJ2aip7qu9JIYsrnKTMUUD7zTI-tqH0lXnxgJEBH2pAz9BPRi5GrjCj4k4xWGUJ6dXvcCQb8RYvH-LThGBjKDwSIkEIZcbNL5tisQWdRpU5xCu9Ig="  # noqa: E501
template_tag_regex = re.compile(r"src='localhost/(?P<encrypted_data>\S+)/' width=1")

test_record = MagicMock()
django_engine = engines["django"]


class TestTrackingPixel(ptrack.TrackingPixel):
    """Test Tracking Pixel class."""

    def record(self, request, *args, **kwargs):
        """Record method for test tracking pixel class."""
        test_record(*args, **kwargs)


ptrack.tracker.register(TestTrackingPixel)


def generate_template_tag_param_str(*args, **kwargs):
    """Test return query string from supplied args and kwargs."""
    param_str = ""
    for arg in args:
        param_str += f"'{arg}' "
    for key, value in kwargs.items():
        param_str += f"{key}='{value}' "
    return param_str


class PtrackViewsTest(TestCase):
    """Tests for Ptrack views."""

    csrf_checks = False

    def test_pixel_image_is_valid(self):
        """Test if the transparent 1 Pixel GIF file is recognised as a GIF."""
        with NamedTemporaryFile() as fp:
            fp.write(TRANSPARENT_1_PIXEL_GIF)
            fp.flush()
            what = imghdr.what(fp.name)
        self.assertEqual("gif", what)

    def test_app_is_accessible(self):
        """Test that the URL is accessible and returns a valid response code."""
        url = reverse("ptrack", kwargs={"ptrack_encoded_data": _test_encrypted_str})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_random_decrypt_fails(self):
        """
        Test that random non encrypted data is ignored.

        Note this test will fail due to incorrect length of data.
        """
        url = reverse("ptrack", kwargs={"ptrack_encoded_data": "thisisnotencryptedata"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_registered_tracker_in_trackers(self):
        """Test that test tracker is registered."""
        matched = False
        for _registered_tracker_name, registered_tracker in ptrack.tracker._registry.items():
            if registered_tracker.__class__ == TestTrackingPixel:
                matched = True
        self.assertEqual(matched, True)

    def test_registered_tracker_used(self):
        """Test that registered trackers are called with valid encrypted data."""
        for test_args in _test_data_params:
            encrypted_data = ptrack.ptrack_encoder.encrypt(*test_args["args"], **test_args["kwargs"])
            url = reverse("ptrack", kwargs={"ptrack_encoded_data": encrypted_data})
            self.client.get(url)
            test_record.assert_called_with(*test_args["args"], **test_args["kwargs"])

    def test_template_tag(self):
        """Test that the template tag generates correctly."""
        for test_args in _test_data_params:
            template_tag_str = generate_template_tag_param_str(*test_args["args"], **test_args["kwargs"])
            template_str = f"{{% load ptrack %}}{{% ptrack {template_tag_str} %}}"
            template_result = django_engine.from_string(template_str).render()

            encrypted_str = template_tag_regex.search(template_result).group(1)
            decrypted_data = ptrack.ptrack_encoder.decrypt(encrypted_str)
            self.assertEqual(decrypted_data[0], test_args["args"])
            self.assertEqual(decrypted_data[1], test_args["kwargs"])
