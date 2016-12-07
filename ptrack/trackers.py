import ptrack
import inspect

class Tracker(object):
    """
    An PtrackSite object encapsulates an instance of the Django ptrack application, ready
    to be hooked in to your URLconf. Models are registered with the PtrackSite using the
    register() method.
    """

    def __init__(self, name='ptrack'):
        self._registry = {}  # (class_name, class_instance)
        self.name = name

    def register(self, custom_ptrack_class):
        if inspect.isclass(custom_ptrack_class) == False:
            raise Exception(custom_ptrack_class + "is not a class, must inherit from ptrack.TrackingPixel")
        if custom_ptrack_class.__name__ in self._registry:
            raise Exception("ptrack already has class "+ custom_ptrack_class.__name__+" registered")
        elif issubclass(custom_ptrack_class, ptrack.TrackingPixel) == False:
            raise Exception(custom_ptrack_class.__name__ + "does not inherit from ptrack.TrackingPixel")
        else:
            self._registry[custom_ptrack_class.__name__] = custom_ptrack_class()

    def call_callbacks(self,*args,**kwargs):
        for key, instance in self._registry.items():
            instance.record(*args,**kwargs)

tracker = Tracker()
