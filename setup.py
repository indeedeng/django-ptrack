__author__ = "Richard Latimer"
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='django-ptrack',
    version='2.1.0',
    description='Ptrack is a tracking pixel library for Django',
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
        'Framework :: Django :: 2.0',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
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
)
