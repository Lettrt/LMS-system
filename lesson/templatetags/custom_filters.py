from django import template
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

register = template.Library()

@register.filter(name='get')
def get(dictionary, key):
    if not isinstance(dictionary, dict):
        return ''
    return dictionary.get(key)