# custom_filters.py
from django import template

register = template.Library()

@register.filter
def custom_range(value, end):
    # Generate a range from value to the end (inclusive)
    return range(value, end + 1)


