# Django Pixel Tracking

Generates a unique tracking pixel per arg/kwargs set. Great for detecting email open rates.

Requires an implementation TrackingPixel to define behavior and registration with ptrack.

Add ptrack to your installed apps:

    INSTALLED_APPS = (
        ...,
        'ptrack',
        ...
    )

Define a secret that is 32-bytes or fewer:
    PTRACK_SECRET = ""

In templates:
    
    {% load ptrack %}
    {% ptrack 'arg' key1='arg1' key2='arg2' ... %}

When this is exploded, it'll generate a tracking pixel of form
    <img src="{{ENCRYPTED_URL}}" width=1 height=1>

In your project, create a file called pixels.py, define the tracking functionality, by overriding base class, defining the record() method, and registering the new class:
    
    import ptrack
    class CustomTrackingPixel(ptrack.TrackingPixel):
        def record(self, *args, **kwargs):
            for arg in args:
                log.info(arg)
            for key, value in kwargs:
                if key == "testemail1":
                    log.info("Recorded test email")
                else:
                    log.info(key + ":" + value)
                
    ptrack.site.register(CustomTrackingPixel)

The record() method is a callback that is executed whenever your tracking pixel is loaded. You can register multiple definitions of ptrack.TrackingPixel to chain callbacks, although there is no gaurantee of the order they will execute. A technical detail is that the tracking response will not complete until all the record() methods have finished executing, so you shouldn't run any long running blocking processes.

In url.py:

    url('^ptrack/', include('ptrack.urls')),


# Validation requirements
    Ptrack won't run the callbacks if someone is trying to guess a url endpoint. It will ignore anything it can't decrypt or serialize.

