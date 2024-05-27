import pprint
from app.models import *
from student.models import *
from exam.models import *
from algorithms import plots


def student_module_test(student):
    modules = student.module_exams.all()
    module_names = []
    note = []
    if len(modules) > 0:
        exam = [Exam.objects.filter(student=student,module = module) for module in modules ]
        for i in range(len(modules)):
            module_names.append(modules[i].name)
            s = 0
            for j in exam[i]:
                s += j.note
            print(f"{s}- {len(exam[i])}")
            note.append(s / len(exam[i]))

        return plots.polar_area_chart_data(
                module_names,
            [note],
            "Your Grade "
        )
    # return plots.polar_area_chart_data([],[[]])
MAX = 0
module_dict = {}
def module_subjects(student: Student):
    global MAX ,module_dict
    courses = student.courses_exams.all()
    module_dict = {}
    for course in courses:
        sub = Subject_answers_for_student.objects.get(student=student,course=course)
        if course.module.name in module_dict:
            module_dict[course.module.name].append(
                [
                    course.name,
                    (sub.correct_answers * 20)
                    / (sub.correct_answers + sub.wrong_answers),
                    sub.time_taking / 1000,
                ]
            )
        else:
            module_dict[course.module.name] = [
                [
                    course.name,
                    (sub.correct_answers * 20)
                    / (sub.correct_answers + sub.wrong_answers),
                    sub.time_taking/1000,
                ]
            ]
    nb_module_dict = {}
    for key in module_dict:
        nb_module_dict[key] = len(module_dict[key])
        if nb_module_dict[key] > MAX:
            MAX = nb_module_dict[key]

    return plots.pie_chart_data(
        list(nb_module_dict.keys()), [list(nb_module_dict.values())], "Subjects "
    )
    # return module_dict

def mean_note_of_course(student:Student):
    global module_dict
    courses = student.courses_exams.all()

    courses = list(module_dict.keys())    
    subjects = []
    values = []
    for val in list(module_dict.values()):
        sub = []
        value = []
        for subject in val:
            value.append(subject[1])
            sub.append(subject[0])
        subjects.append(sub)
        values.append(value)

    return courses, [ plots.bar_chart_data(subjects[i],[values[i]],["Your Grade (/20)"]) for i in range(len(subjects))]
    # pprint.pprint(list(module_dict.values())[0][1])


def time_taking_of_course(student: Student):
    global module_dict
    courses = student.courses_exams.all()

    courses = list(module_dict.keys())
    subjects = []
    values = []
    for val in list(module_dict.values()):
        sub = []
        value = []
        for subject in val:
            value.append(subject[2])
            sub.append(subject[0])
        subjects.append(sub)
        values.append(value)

    return courses, [
        plots.bar_chart_data(subjects[i], [values[i]], ["Time Taking (S) "])
        for i in range(len(subjects))
    ]
