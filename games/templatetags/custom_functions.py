from django import template

register = template.Library()

@register.filter
def concatstr(arg1, arg2):
    return str(arg1) + str(arg2)