
'''
from django import template

register = template.Library()

@register.filter(name='yes_no')
def yes_no(value):
    if value == 1:
        return "Yes"
    elif value == 0:
        return "No"
    return value
'''