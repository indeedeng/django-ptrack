"""
Compatibility module for encapsulating dependencies that moved between Django 1.11 and 2.2.
"""
try:
    # Try Django 2.x import first:
    from django.urls import reverse  # noqa
except ImportError:
    from django.core.urlresolvers import reverse  # noqa
