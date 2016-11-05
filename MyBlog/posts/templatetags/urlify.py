from urllib import parse
from django import template
register = template.Library()
@register.filter
def urlify(value):
    return parse.quote(value)