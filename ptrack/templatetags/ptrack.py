from django import template
from ..utils import encrypt
from django.core.urlresolvers import reverse
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def ptrack(context, *args, **kwargs):
    sub_path = reverse('ptrack', kwargs={'ptrack_encoded_data':encrypt(*args,**kwargs)})
    
    if settings.PTRACK_APP_URL:
        url = "%s%s" % (settings.PTRACK_APP_URL, sub_path)
    else:
        raise Error("PTRACK_APP_URL not defined")

    return "<img src='%s' width=1 height=1>" % (url,)