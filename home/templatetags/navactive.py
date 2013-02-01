import re

from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(request, url):
    ret = ''
    
    if re.search(url, request.path):
        ret = 'active'

    return ret
