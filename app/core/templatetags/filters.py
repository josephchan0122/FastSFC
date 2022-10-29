from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter(name='size')
def size(value):
    if value == -1:
        return '-'
    return intcomma(value) + ' kb'


@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')


@register.filter
def percentage(value, decimals):
    string = '{0:.' + str(decimals) + '%}'
    return string.format(value)