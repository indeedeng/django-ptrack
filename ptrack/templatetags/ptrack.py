
register = template.Library()


@register.simple_tag
def ptrack(a, b, *args, **kwargs):
    return "<img src='' width=1 height=1>"