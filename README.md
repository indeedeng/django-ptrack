# Django Pixel Tracking

Generates a unique tracking pixel per arg/kwargs set. Requires a single instantiation of TrackingPixelBase to define behavior and the class registered with ptrack.

In templates:
    
    {% ptrack 'arg1' key1='arg2' ... %}

In views, define the tracking functionality, by overriding base class:
    
    import ptrack
    class CustomTrackingPixel(ptrack.TrackingPixelBase):
        def __init__(self, *args, **kwargs):
            for arg in args:
                log.info(arg)
            for keys, values in kwargs:
                log.info(keys + ":" + values)
    ptrack.register(CustomTrackingPixel)
    
Tracking pixel will automatically be added to:

    "/ptrack/(?P<key>)" as part of your app.