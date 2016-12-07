__author__ = "Richard Latimer"
from setuptools import setup, find_packages

version = '0.0.1'

setup(
    name='ptrack',
    version=version,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'example_project']),
    install_requires=[
    'Django>=1.8.1',
    'pycrypto>=2.6.1',
    ],
)
