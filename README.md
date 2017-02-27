# Django Ptrack
Ptrack is a track pixel library for Django. Ptrack is great for detecting email open rates or creating your own pixel tracking API. Here at Indeed.com, ptrack generates tracking pixels with an average request to response lifecycle that is consistently < 80 ms.

Each tracking pixel is a unique encoded image generated per arg/kwargs set. Unlike other tracking pixel libraries, Ptrack is stateless and does not require a database. Instead, ptrack providers the developer the ability to pass in meta data which is encrypted and store in the img url. 


Pip install:

    django-ptrack

Add ptrack to your installed apps in settings:

    INSTALLED_APPS = (
        ...,
        'ptrack',
        ...
    )

Define a secret that is 32-bytes or fewer:

    PTRACK_SECRET = ""

Define the app url for ptrack

    PTRACK_APP_URL = ""

Note: One benefit of the PTRACK_APP_URL is that if you want pixel tracking on emails sent from a web app hosted on an internal network, can create a public facing mirror web app that records the pixels. As long as the internal app and external app both share the same PTRACK_SECRET and are registered on the same url path prefix, it should just work.

In templates:

    {% load ptrack %}
    {% ptrack 'arg' key1='arg1' key2='arg2' ... %}

When this is tag is expanded, it'll generate a tracking pixel of form

    <img src="{{ENCRYPTED_URL}}" width=1 height=1>

Ptrack will automatically search your project for a file called pixels.py, which is where you register your pixel tracking callbacks.

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
     
    ptrack.tracker.register(CustomTrackingPixel)


The record() method is a callback that is executed whenever your tracking pixel is loaded. You can register multiple definitions of ptrack.TrackingPixel to chain callbacks, although there is no gaurantee of the order they will execute. A technical detail is that the tracking response will not complete until all the record() methods have finished executing, so you shouldn't run any long running blocking processes.

In url.py, register 'ptrack.urls' on your desired url prefix pattern:

    url('^ptrack/', include('ptrack.urls')),


# Validation requirements
    Ptrack won't run the callbacks if someone is trying to guess a url endpoint. It will ignore anything it can't decrypt or deserialize.

# Notes
* When testing locally, the tracking pixel will show an empty box rather than be invisible, because gmail can't handle reading from localhost
* It's best to include the tracking pixel at the bottom of an email or page, because if the server has downtime, the pixel will become visible as an empty box.
* Realize that your encoded meta data tied to the tracking pixel is stored in the URL. A good rule of thumb is that the # of characters you store should be less than 0.5 * (the maximum character limit of the browser you want to support)

# Testing
Navigate to the ptrack directory on your local machine and run

    python setup.py test

# Adding an encoder
While ptrack should work out of the box, you have the ability to create your own encoder. Suppose you created a class MyEncoder, with a static encrypt and decrypt methods. In your application's pixels.py, you could then register the encoder with:

    import ptrack
    ptrack.ptrack_encoder = MyEncoder
