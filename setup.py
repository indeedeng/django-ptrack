__author__ = "Richard Latimer"
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='django-ptrack',
    version='1.1.0',
    description='A sample Python project',
    long_description=long_description,

    url='https://github.com/indeedeng/django-ptrack',

    author='Richard Latimer, Sarah Ellis',
    author_email='rlatimer@indeed.com, sellis@indeed.com',

    license='Apache',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='django',

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
