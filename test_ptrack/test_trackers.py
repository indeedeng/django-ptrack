import unittest

import pytest

import ptrack
from ptrack.exceptions import PtrackRegistrationError
from ptrack.trackers import Tracker


class TestTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = Tracker()

    def test_registration_fails_if_object_is_not_a_class(self):
        not_a_class = "not-a-class"
        with pytest.raises(PtrackRegistrationError, match="not-a-class is not a class, .*"):
            self.tracker.register(not_a_class)

    def test_registration_fails_if_already_registered(self):
        class FakePixel(ptrack.TrackingPixel):
            def record(self, request, *args, **kwargs):
                pass

        self.tracker.register(FakePixel)
        with pytest.raises(PtrackRegistrationError, match="ptrack already has class FakePixel .*"):
            self.tracker.register(FakePixel)

    def test_registration_fails_if_not_subclass_of_tracking_pixel(self):
        class FakePixel:
            def record(self, request, *args, **kwargs):
                pass

        with pytest.raises(PtrackRegistrationError, match="FakePixel does not inherit .*"):
            self.tracker.register(FakePixel)
