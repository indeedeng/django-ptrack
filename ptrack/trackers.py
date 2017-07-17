""" Ptrack Tracker: TrackingPixel registry and tracker """
import inspect
import ptrack


class Tracker(object):
    """
    A Tracker object encapsulates an instance of the Django ptrack application, ready
    to be hooked in to your URLconf. TrackingPixel callbacks are registered with the
    Tracker PtrackSite using the register() method.
    """

    def __init__(self, name='ptrack'):
        """ Set up the tracking TrackingPixel registry and tracker name """
        self._registry = {}  # {class_name: class_instance}
        self.name = name

    def register(self, trackingpixel_callback):
        """ Register a new TrackingPixel """
        if inspect.isclass(trackingpixel_callback) is False:
            raise Exception(trackingpixel_callback + "is not a class, must inherit from ptrack.TrackingPixel")
        elif trackingpixel_callback.__name__ in self._registry:
            raise Exception("ptrack already has class " + trackingpixel_callback.__name__ + " registered")
        elif issubclass(trackingpixel_callback, ptrack.TrackingPixel) is False:
            raise Exception(trackingpixel_callback.__name__ + "does not inherit from ptrack.TrackingPixel")
        else:
            self._registry[trackingpixel_callback.__name__] = trackingpixel_callback()

    def call_callbacks(self, request, *args, **kwargs):
        """ Call each registered TrackingPixel's record method """
        for _, instance in self._registry.items():
            instance.record(request, *args, **kwargs)

tracker = Tracker()
