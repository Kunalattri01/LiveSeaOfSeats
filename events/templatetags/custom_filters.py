from django import template


register = template.Library()

@register.filter
def split(values, separator = ','):
    return values.split(separator)


@register.filter
def dict(value):
    return dict(value)