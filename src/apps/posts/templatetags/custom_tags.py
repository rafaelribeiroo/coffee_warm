from django import template
import re

register = template.Library()


@register.filter
def img_exclude(value):
    return re.sub(r'<img[^>]*?>', '', value)
