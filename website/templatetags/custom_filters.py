# custom_filters.py

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='highlight')
@stringfilter
def highlight(value, query):
    return value.replace(query, f'<span class="highlight">{query}</span>')
