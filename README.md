# Django Ptrack

![OSS Lifecycle](https://img.shields.io/osslifecycle/indeedeng/django-ptrack.svg)

Ptrack is a tracking pixel library for Django.

You can use Ptrack to detect email open rates or to create your own pixel tracking API.
When used by Indeed, Ptrack generates pixels with average request to response lifecycles of <80 ms.

Each tracking pixel is a unique encoded image generated per arg/kwargs set.
Unlike other tracking pixel libraries, Ptrack is stateless and does not require a database.
Instead, ptrack allows developers to pass in metadata which is encrypted and stored in the image url.

## Getting Started
Install the library using Pip:
```
pip install django-ptrack
```

### Configuration
1. Add Ptrack to your installed apps in settings:
```
INSTALLED_APPS = (
    ...,
    'ptrack',
    ...
)
```

2. Define a secret that is 32-character bytes or fewer.
The secret is used to create an encrypted tracking pixel url.
```
PTRACK_SECRET = ""
```

3.  Define a Ptrack app URL in your settings. This is the domain that the tracking pixel will be based on.
```
PTRACK_APP_URL = "" # Example: PTRACK_APP_URL = "https://www.example.com"
```

*NOTE:* The PTRACK_APP_URL gives you a lot of flexibility.
For example, if you are trying to track emails from a web app hosted on an internal network, you can deploy a public facing mirror web app that records the pixels.
As long as the internal and external apps share the same secret and are registered on the same URL path prefix, tracking should work.



## Using Ptrack
Load and define Ptrack in templates:
```
{% load ptrack %}
{% ptrack 'arg' key1='arg1' key2='arg2' ... %}
```

When the ptrack template tag is expanded, it generates a tracking pixel of form:
```
<img src="{{ENCRYPTED_URL}}" width=1 height=1>
```

*NOTE:*
* Keep in mind that valid arg and kwarg values must be json serializable ints or strings.
If non-valid inputs are provided, the template tag will throw an exception.
* When testing a tracking pixel in an email locally or with a domain that is not publicly accessible, the tracking pixel in the email will appear as an empty box rather than as an invisible pixel.
The reason the image is rendered as an error image is because most email servers, such as Gmail, will proxy img tags.
* If the server has downtime, the pixel appears as an empty box.
For this reason, it is best to include the tracking pixel at the bottom of an email or page.
* Realize that the encoded metadata tied to the tracking pixel is stored in the URL.
As a best practice, the number of characters you store should be less than half the maximum character limit of your supported browser.


### Define tracking functionality
Ptrack automatically searches your project for a file called `pixels.py`, in which you register your pixel tracking callbacks.

Create this file in your project.
Define the tracking functionality by overriding base class, defining the record() method, and registering the new class:
```
import ptrack
class CustomTrackingPixel(ptrack.TrackingPixel):
    def record(self, request, *args, **kwargs):
        log.info(request.META['HTTP_USER_AGENT'])
        for arg in args:
            log.info(arg)
        for key, value in kwargs:
            if key == "testemail1":
                log.info("Recorded test email")
            else:
                log.info(key + ":" + value)

ptrack.tracker.register(CustomTrackingPixel)
```

Whenever your tracking pixel is loaded, the record() callback method is executed.

### Define multiple callbacks
You can register multiple definitions of `ptrack.TrackingPixel` to chain callbacks, although there is no guarantee of the order they will execute.

*NOTE:* The tracking response will not complete until all the record() methods have finished executing, so you shouldn't run any long running blocking processes.

### Register ptrack.urls
In `url.py`, register 'ptrack.urls' on your desired url prefix pattern:
```
url('^ptrack/', include('ptrack.urls')),
```

### Tracking dictionary values in template tag
The general use of `ptrack` as a template tag is:
```
{% ptrack key1=value1 key2=value2 %}
```
However, doing above requires explicity writing out all key value pairs. If the template context contains a field having dictionary type data (example: `dict_field = {"df_key1": "df_value", "df_key2": 2}`), or field that references a model object with a property method that returns a dictionary type data (example: `model_field = model`, such that `model.dict_property` returns `{"model_key1": "model_key", "model_key2": 3}`), then it is possible to collect these values within `ptrack` by passing them as positional arguments to the `ptrack` template tag, like:
```
{% ptrack dict_field model_field.dict_property key1=value1 key2=value2 %}
```
Additionally, the `CustomTrackingPixel.record` method must be modified to read the positional arguments and include them with the keyworded arguments, like:
```
import ptrack
class CustomTrackingPixel(ptrack.TrackingPixel):
    def record(self, request, *args, **kwargs):
        args_updated_dict = { **kwargs }
        for arg in args:
            if instance(arg, dict):
                args_updated_dict.update(arg)
            else:
                log.info(arg)
        # Below, `args_updated_dict` includes keywords from both `kwargs` and dictionary type `arg` argument
        for key, value in args_updated_dict:  
            log.info(key + ":" + value)

ptrack.tracker.register(CustomTrackingPixel)
```

### Capturing time to open
It is possible to accommodate use case where it is needed to identify the time between when tracking pixel was created to when it gets activated. For example, the time difference between when an email containing the tracking pixel is created to when the user opens it. To do so, a numeric values `pixel_create_time` can be added in the `ptrack` template tag, and `CustomTrackingPixel.record` method can be modified to read the `pixel_create_time` and evaluate the time difference since then. This is assuming that the email was sent as soon as it was rendered.

## Validation requirements
Ptrack ignores anything it cannot decrypt or deserialize.
Callbacks are not run if someone attempts to guess a URL endpoint.


## Testing
To build tests, navigate to the ptrack directory on your local machine and run `tox`. Install tox if neccesary with `pip install tox`.

## Overriding the encoder
While ptrack should work out of the box, you have the ability to create your own encoder.

Suppose you created a class MyEncoder, with _static_ `encrypt` and `decrypt` methods.
In your application's `pixels.py`, you then register the encoder:
```
import ptrack
ptrack.ptrack_encoder = MyEncoder
```

## Installation Errors
If you run into installation errors, such as:
```
distutils.errors.DistutilsError: Setup script exited with error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
```

You may need to install system dependencies for PyNacl:
```
sudo apt-get install python-dev
sudo apt-get install libffi-dev
```

## Code of Conduct
This project is governed by the [Contributor Covenant v 1.4.1](CODE_OF_CONDUCT.md)

## License
This project uses the [Apache 2.0](LICENSE.txt) license.
