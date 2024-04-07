import random
from django.http import HttpResponse
from django.shortcuts import render

from app.classes.student import Student_class
from .classes.functions import *


# initialization
std = Student_class()
std.get_student(1)

student = std.student
questions = None
sampler = None
context = None

# request


def home(request):
    get_data_from_db("Math", "multuplication one number", "qcm")
    return render(
        request,
        "home.html",
        {"courses": get_courses(), "student": std.student.name},
    )

def module(request, module_name):
    return render(
        request, "module.html", {"courses": get_courses(), "student": std.student.name ,"module_name":module_name}
    )

def courses(request, module_name, course_name):
    return render(request, "module.html")
# add upper alpha before the  items of the list


def prepare_exam(request, module_name, course_name):
    global questions, sampler, context

    if request.method == "POST":
        if request.POST.get("submit") == "Submit":
            index_question = int(request.POST.get("arm"))
            time_taken = float(request.POST.get("time"))
            answer = request.POST.getlist("answer[]")
            question_treatment(
                answer, questions, index_question, time_taken, sampler
            )
            context["feedback"] = get_feedback(index_question, questions, answer)
            context['state'] = False
            context['answer'] = answer
            context['results'] = get_stats(sampler, questions)
        else:
            context = get_context(sampler, questions, student)
        return render(
            request,
            "q_learning_tmp.html",
            context = context,
        )
    questions, sampler, arm, question, possible_choses = init_variables(module_name, course_name, std, function=0)
    context = {
        "courses": get_courses(),
        "question": question,
        "possible_choses": add_upper_alpha(
            random.sample(possible_choses, len(possible_choses))
        ),
        "arm": arm,
        "feedback": [0, ""],
        "results": get_stats(sampler, questions),
        "student": std.student.name,
        "state": True,
        'answer': []
    }
    return render(
        request,
        "q_learning_tmp.html",
        context=context,
    )

def upload_json_file(request):
    with open(
        "/home/mr-abdelhake/Documents/projetFE/ITS_Programme_interface(QCM)/exam_pfe/app/data.json",
        "r",
    ) as file:
        load_data_as_json(file)
    return HttpResponse("done")
