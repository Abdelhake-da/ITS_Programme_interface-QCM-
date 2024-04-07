from django import template

from app.classes.functions import get_data_from_db

register = template.Library()


@register.filter
def concat(value, arg):
    return str(arg) + str(value)


@register.filter
def get_item(dictionary, key):
    print(dictionary)
    return dictionary.get(key)


@register.filter
def in_list(value, the_list):
    return str(value) in the_list


@register.filter
def get_questions_len(module_name, course_name):
    return len(get_data_from_db(module_name, course_name, "qcm"))
