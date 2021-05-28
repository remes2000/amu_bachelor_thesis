from urllib.parse import urlencode
from django import template

register = template.Library()


@register.simple_tag
def get_value_from_dict(dictionary, key):
    return dictionary[key]


@register.simple_tag
def get_number_of_notifications(user):
    return user.notification_set.filter(is_seen=False).count()


@register.simple_tag
def has_notifications(user):
    return user.notification_set.filter(is_seen=False).count() == 0
