"""Ptrack Template Tag"""
from django import template
from django.urls import reverse
from django.conf import settings
from .. import ptrack_encoder
from django.utils.html import mark_safe

register = template.Library()


@register.simple_tag
def ptrack(*args, **kwargs):
    """Generate a tracking pixel html img element."""
    if settings.PTRACK_APP_URL:
        encoded_dict = {'ptrack_encoded_data': ptrack_encoder.encrypt(*args, **kwargs)}
        sub_path = reverse('ptrack', kwargs=encoded_dict)

        url = "%s%s" % (settings.PTRACK_APP_URL, sub_path)
    else:
        raise Exception("PTRACK_APP_URL not defined")

    return mark_safe(
        '<img src="%s" width="1" height="1" alt="" border="0" style="height:1px;width:1px;border:0;" />' % (url,))
