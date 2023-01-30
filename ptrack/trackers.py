"""Ptrack TrackingPixel registry and tracker."""
import inspect
import logging

import ptrack

from .exceptions import PtrackRegistrationError

logger = logging.getLogger(__name__)


class Tracker:
    """
    A Tracker object encapsulates an instance of the Django ptrack application, ready to be hooked in to your URLconf.

    TrackingPixel callbacks are registered with the Tracker PtrackSite using the register() method.
    """

    def __init__(self, name="ptrack"):
        """Set up the tracking TrackingPixel registry and tracker name."""
        self._registry = {}  # {class_name: class_instance}
        self.name = name

    def register(self, trackingpixel_callback):
        """Register a new TrackingPixel."""
        if inspect.isclass(trackingpixel_callback) is False:
            msg = trackingpixel_callback + " is not a class, must subclass ptrack.TrackingPixel"
            raise PtrackRegistrationError(msg)

        elif trackingpixel_callback.__name__ in self._registry:
            msg = "ptrack already has class " + trackingpixel_callback.__name__ + " registered"
            raise PtrackRegistrationError(msg)

        elif issubclass(trackingpixel_callback, ptrack.TrackingPixel) is False:
            msg = trackingpixel_callback.__name__ + " does not inherit from ptrack.TrackingPixel"
            raise PtrackRegistrationError(msg)

        else:
            self._registry[trackingpixel_callback.__name__] = trackingpixel_callback()
            logger.debug(f"ptrack registered {self._registry[trackingpixel_callback.__name__]=}")

    def call_callbacks(self, request, *args, **kwargs):
        """Call each registered TrackingPixel's record method."""
        for _, instance in self._registry.items():
            logger.debug(f"ptrack callback record {_=}")
            instance.record(request, *args, **kwargs)


tracker = Tracker()
