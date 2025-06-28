# hotel/templatetags/peso_filters.py

from django import template
from django.template.defaultfilters import floatformat
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def peso(value):
    try:
        value = float(value)
        return f"₱{intcomma(floatformat(value, 2))}"
    except (ValueError, TypeError):
        return value
