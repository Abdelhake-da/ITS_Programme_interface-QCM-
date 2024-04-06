import random
from django.http import HttpResponse
from django.shortcuts import render

from app.classes.student import Student_class
from .classes.functions import *


# initialization
std = Student_class()
std.get_student(1)
print()
student = std.student
questions = None
sampler = None

# request


def home(request):
    get_data_from_db("Math", "multuplication one number", "qcm")
    return render(
        request,
        "home.html",
        {"courses": get_courses(), "student": std.student.name},
    )

def module(request, module_name):
    return render(request, "module.html")

def courses(request, module_name, course_name):
    return render(request, "module.html")

def prepare_exam_q_learning(request, module_name, course_name):
    global questions, sampler
    if request.method == "POST":
        index_question = int(request.POST.get("arm"))
        time_taken = float(request.POST.get("time"))
        answer = request.POST.getlist("answer[]")
        return render(
            request,
            "q_learning_tmp.html",
            question_treatment(
                answer, questions, index_question, time_taken, sampler, std.student
            ),
        )
    questions, sampler, arm, question, possible_choses = init_variables(module_name, course_name, std, function=0)
    return render(
        request,
        "q_learning_tmp.html",
        {
            "courses": get_courses(),
            "question": question,
            "possible_choses": random.sample(possible_choses, len(possible_choses)),
            "arm": arm,
            "feedback": [0, ""],
            "results": get_feedback(sampler, questions),
            "student": std.student.name,
        },
    )

def upload_json_file(request):
    with open(
        "/home/mr-abdelhake/Documents/projetFE/ITS_Programme_interface(QCM)/exam_pfe/app/data.json",
        "r",
    ) as file:
        load_data_as_json(file)
    return HttpResponse("done")


"""
    def prepare_exam(request, module_name, course_name):
    global questions, sampler
    if request.method == "POST":
        time_taken = float(request.POST.get("time"))
        answer = request.POST.getlist("answer[]")
        correct_answer = questions[int(request.POST.get("arm"))]["correct_answer"]
        success = is_correct(answer, correct_answer)
        sampler.update(int(request.POST.get("arm")), success, time_taken)

        feedback = (
            [0, "You answered correctly!"]
            if success
            else [1, solution(questions[int(request.POST.get("arm"))])]
        )
        arm = sampler.select_arm()
        question = questions[arm]["question"]
        possible_choses = questions[arm]["possible_choses"]
        results = []
        for i, q in enumerate(questions):
            incorrect = sampler.failures[i]
            correct = sampler.successes[i]
            times = sampler.times[i]
            total_time = sum(times)
            avg_time = total_time / len(times) if times else 0

            results.append(
                {
                    "question": q["question"],
                    "correct": correct,
                    "incorrect": incorrect,
                    "max_time": max(times) if times else 0,
                    "min_time": min(times) if times else 0,
                    "average_time": avg_time,
                }
            )

        return render(
            request,
            "index_copy copy.html",
            {
                "courses": get_courses(),
                "question": question,
                "possible_choses": random.sample(possible_choses, len(possible_choses)),
                "arm": arm,
                "feedback": feedback,
                "results": results,
            },
        )
    questions, sampler, arm, question, possible_choses = init_variables(
        module_name, course_name, std.student
    )
    return render(
        request,
        "index_copy copy.html",
        {
            "courses": get_courses(),
            "question": question,
            "possible_choses": random.sample(possible_choses, len(possible_choses)),
            "arm": arm,
            "feedback": [0, ""],
        },
    )

"""
