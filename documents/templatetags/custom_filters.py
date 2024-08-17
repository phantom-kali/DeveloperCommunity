from django import template

register = template.Library()

@register.filter
def equal(value, arg):
    return value == arg
