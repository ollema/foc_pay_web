from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def clean_phone_number(phone_number):
    return "0" + phone_number[2:]  # Replace 46 with 0
