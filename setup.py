__author__ = "Richard Latimer"
from setuptools import setup, find_packages

version = '1.1.0'

setup(
    name='django-ptrack',
    version=version,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'example_project']),
    install_requires=[
        'Django>=1.8.1',
        'pynacl>=1.0.1'
    ],
    extras_require={
        'legacy': ['pycrypto>=2.6.1']
    },
    tests_require=[
        'nose==1.3.7',
        'mock==2.0.0',
        'django-webtest==1.8.0',
        'coverage==4.3.',
        'pylint==1.6.5'
    ],
    test_suite="test_ptrack.run_tests.run_all",
)
