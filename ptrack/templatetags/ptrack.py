from django import template
from ..utils import encrypt
from django.core.urlresolvers import reverse


register = template.Library()


@register.simple_tag(takes_context=True)
def ptrack(context, *args, **kwargs):
    sub_path = reverse('ptrack', kwargs={'ptrack_encoded_data':encrypt(*args,**kwargs)})
    url = context['request'].build_absolute_uri(sub_path)
    return "<img src='%s' width=1 height=1>" % (url,)