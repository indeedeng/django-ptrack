"""Ptrack Simple Template Tag."""
import logging

from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.utils.html import mark_safe

from ptrack import ptrack_encoder

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def ptrack(*args, **kwargs):
    """Generate a tracking pixel html img element."""
    if settings.PTRACK_APP_URL:
        encoded_dict = {"ptrack_encoded_data": ptrack_encoder.encrypt(*args, **kwargs)}
        sub_path = reverse("ptrack", kwargs=encoded_dict)

        url = f"{settings.PTRACK_APP_URL}{sub_path}"
    else:
        raise ImproperlyConfigured("PTRACK_APP_URL not defined")

    logger.debug(f"Ptrack tag generated URL: {url}")
    return mark_safe(
        f'<img src="{url}" width="1" height="1" alt="" border="0" style="height:1px;width:1px;border:0;" />'
    )
