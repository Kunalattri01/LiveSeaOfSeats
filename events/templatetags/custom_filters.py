from django import template
import re

register = template.Library()

@register.filter
def split(values, separator = ','):
    return values.split(separator)


@register.filter
def dict(value):
    return dict(value)


@register.filter
def country_code(value):
    match = re.search(r"\((.*?)\)", value)
    return match.group(1).lower() if match else ""