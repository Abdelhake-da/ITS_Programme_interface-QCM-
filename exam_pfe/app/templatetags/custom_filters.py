import pprint
import uuid
from django import template
register = template.Library()


@register.filter
def add_one(value):
    return int(value)+1


@register.filter
def get_num(index,questions):
    return len(questions[index])


@register.simple_tag
def generate_unique_id():
    unique_id = str(uuid.uuid4()).replace("-", "")
    return "exam-" + unique_id[: 30 - len("exam")]
@register.filter
def set_id(index,index_ch):
    return f"choice-{index}-{index_ch}"


@register.filter
def set_id_question(index):
    return f"question-{index}"


@register.filter
def add_one(value):
    return int(value)+1

@register.filter
def add_num_to_answers(index):
    return f"answer{index}[]"


@register.filter
def is_in_answers(lis,value):
    """
    0 = not in answers
    1 = in answers but wrong
    2 = in answers but correct
    """
    print("===========================================")
    pprint.pprint(lis)
    # print(lis[0], " - ", value, " - ", lis[1])
    print("===========================================")
    # return value in answers[question]
    return str(value) in lis[0][lis[1]]


@register.filter
def append(v1,v2):
    lis = [v1,v2]
    # print('------------------------------------------')
    # print(lis)
    # print("------------------------------------------")
    return lis


@register.filter(name="my_custom_filter")
def my_custom_filter(value, arg1, arg2=""):
    # Filter logic
    result = value + " " + arg1 + " " + arg2
    return result
