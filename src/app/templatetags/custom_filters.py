import datetime
import pprint
import uuid
from django import template
from app.models import Course, Question, Module
from student.models import Student
from exam.models import Exam

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
# -------------1----------------------------------------------------------------------------
# -------------1----------------------------------------------------------------------------
# -------------1----------------------------------------------------------------------------
# -------------1----------------------------------------------------------------------------
@register.filter(name="count_numbers")
def number_of_courses_and_questions(value):
    courses = Course.objects.filter(module= Module.objects.get(id = value))
    nb_questions = [len(Question.objects.filter(course= course)) for course in courses]
    return [len(courses),sum(nb_questions)]
@register.filter
def add_attr(field, extra_attrs):
    attrs = dict(field.field.widget.attrs)
    for attr_pair in extra_attrs.split(","):
        attr_name, attr_value = attr_pair.split(":", 1)
        attrs[attr_name] = attr_value
    field.field.widget.attrs = attrs
    return field
@register.simple_tag
def increment(value):
    return value + 1
@register.simple_tag
def get_question(value):
    return Question.objects.get(id=value)
@register.filter
def get_value_from_dict(value, dic):
    return dic[value]
@register.filter
def get_qst_txt(value:Question):
    return value.qst_text
@register.filter
def get_qst_choices(value: Question):
    return value.get_choices()
@register.filter
def get_correct_p_answers(value: Question,answer):
    return [answer, [ int(i) for i in value.get_correct_answer()]]
@register.filter
def check_box(value,lis):
    print(lis[1])
    val = 3
    for i in lis[0] :
        if value == int(i[0]):
            if i[1]:
                return 0
            else:
                return 1
    if value in lis[1]:
        return 2
    return 3
@register.filter
def format_time( ms):
    time_obj = datetime.datetime.utcfromtimestamp(float(ms) / 1000.0)
    return time_obj.strftime("%M:%S.%f")[:-3]
@register.filter
def get_student(user):
    return Student.objects.get(user=user)
@register.filter
def get_date(date):
    return "0000-00-00" if date == None else date.strftime("%Y-%m-%d")
@register.filter
def get_age(date):
    print(date)
    return 0 if date == None else datetime.date.today().year - date.year
@register.filter()
def get_std_info(std:Student):
    return[len(std.module_exams.all()),len(std.courses_exams.all()),len(Exam.objects.filter(student=std))]
@register.filter()
def concatenate(text1, text2):
    return f"{text1}-{text2}"