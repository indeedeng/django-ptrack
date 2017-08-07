import re
from mock import MagicMock
from django.core.urlresolvers import reverse
from django_webtest import WebTest
from django.template import engines
from django.template.loader import render_to_string
import ptrack


# setup
_test_data_params = [
    {
        'args': ['testarg'],
        'kwargs': {'testkey1':'testarg1', 'testkey2':'testarg2'}
    },
    {
        'args': ['thisisalongtestarg1', 'thisisalongtestarg2', 'thisisalongtestarg3', 'thisisalongtestarg4'],
        'kwargs': {'thisisalongtestkey1':'thisisalongtestkwargvalue1', 'thisisalongtestkey2':'thisisalongtestkwargvalue2'}
    },
    {
        'args': ['[][][][]]', '$%^&%%^$'],
        'kwargs': {'one':u'[]][]]', 'two':u'[][][]]'}
    },
    {
        'args': ['testarg1', 'testarg2', 'testarg3'],
        'kwargs': {}
    },
    {
        'args': [],
        'kwargs': {'testkey1':'testarg1', 'testkey2':'testarg2'}
    },

]
_test_encrypted_str = 'Ylk67uIkGhy5_ugiHhAgu0_oG72_S-lSGGfHeZOUjJBJZwzNOYruvZqhnQAnGv93td1YvI5K_W-telcEya7vSEosk66TyW00i5lM2_iWAr995vLjyxaL9Z5qBsG3BRec11mS652MhV2x1whSC35VpP63J-WjEP1ejl8AW68cuduH8HdfQSC6draXF7BWuiha706NYnXtESJDACsBJaUJ2aip7qu9JIYsrnKTMUUD7zTI-tqH0lXnxgJEBH2pAz9BPRi5GrjCj4k4xWGUJ6dXvcCQb8RYvH-LThGBjKDwSIkEIZcbNL5tisQWdRpU5xCu9Ig='
template_tag_regex = re.compile("src='localhost/(?P<encrypted_data>\S+)/' width=1")

test_record = MagicMock()
django_engine = engines['django']


class TestTrackingPixel(ptrack.TrackingPixel):
    def record(self, request, *args, **kwargs):
        test_record(*args, **kwargs)

ptrack.tracker.register(TestTrackingPixel)


def generate_template_tag_param_str(*args, **kwargs):
    param_str = u""
    for arg in args:
        param_str += u"'{}' ".format(arg)
    for key, value in kwargs.iteritems():
        param_str += u"{}='{}' ".format(key, value)
    return param_str


class PtrackViewsTest(WebTest):
    csrf_checks = False

    def test_app_is_accessible(self):
        response = self.app.get(reverse('ptrack', kwargs={'ptrack_encoded_data': _test_encrypted_str}))
        self.assertEqual(response.status_int, 200)

    def test_random_decrypt_fails(self):
        response = self.app.get(reverse('ptrack', kwargs={'ptrack_encoded_data': 'thisisnotencryptedata'}))
        self.assertEqual(response.status_int, 200)

    def test_registered_tracker_in_trackers(self):
        matched = False
        for registered_tracker_name, registered_tracker in ptrack.tracker._registry.iteritems():
            if registered_tracker.__class__ == TestTrackingPixel:
                matched = True
        self.assertEqual(matched, True)

    def test_registered_tracker_used(self):
        for test_args in _test_data_params:
            encrypted_data = ptrack.ptrack_encoder.encrypt(*test_args['args'], **test_args['kwargs'])
            response = self.app.get(reverse('ptrack', kwargs={'ptrack_encoded_data': encrypted_data}))
            test_record.assert_called_with(*test_args['args'], **test_args['kwargs'])

    def test_template_tag(self):
        for test_args in _test_data_params:
            template_tag_str = generate_template_tag_param_str(*test_args['args'], **test_args['kwargs'])
            template_str = u"{{% load ptrack %}}{{% ptrack {} %}}".format(template_tag_str)
            template_result = django_engine.from_string(template_str).render()

            encrypted_str = template_tag_regex.search(template_result).group(1)
            decrypted_data = ptrack.ptrack_encoder.decrypt(encrypted_str)
            self.assertEqual(decrypted_data[0], test_args['args'])
            self.assertEqual(decrypted_data[1], test_args['kwargs'])
