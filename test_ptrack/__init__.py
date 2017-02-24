import os
from django.test.runner import DiscoverRunner

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_ptrack.settings'
test_runner = DiscoverRunner()

import django
django.setup()


# def setup():
#     global test_runner
#
#     from django.test.runner import DiscoverRunner
#
#     test_runner = DiscoverRunner()
    # test_runner.setup_test_environment()
    # not setting up test db - ptrack tests do not require a DB


# def teardown():
#     test_runner.teardown_test_environment()
