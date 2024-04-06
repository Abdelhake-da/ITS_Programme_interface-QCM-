from django import template

register = template.Library()


@register.filter
def concat(value, arg):
    return str(arg) + str(value)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
