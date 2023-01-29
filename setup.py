__author__ = "Richard Latimer"
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='django-ptrack',
    version='3.0.0',
    description='Ptrack is a tracking pixel library for Django',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/indeedeng/django-ptrack',

    author='Richard Latimer, Sarah Ellis',
    author_email='rlatimer@indeed.com, sellis@indeed.com',

    license='Apache',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    keywords='django',

    packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'example_project']),
    install_requires=[
        'Django>=3.2.0',
        'pynacl>=1.0.1'
    ],
    extras_require={
        'legacy': ['pycrypto>=2.6.1']
    },
)
