from urllib.parse import urlencode
from django import template

register = template.Library()


@register.simple_tag
def get_value_from_dict(dictionary, key):
    return dictionary[key]
