import json
import pprint
from typing import List
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from app.models import Course, Module, Question
from student.models import StudentQuestions, Student
from algorithms.thompson_sampler import ThompsonSampler
from django.contrib.auth.decorators import login_required
from exam.models import Exam
# Create your views here.
arms = []
ts: ThompsonSampler = None
STUDENT = None
COURSES = None
MODULE = None
def index(request):
    return render(request, "index.html")
@login_required(login_url="student:login") 
def prepare_exam(request, module_id=''):
    modules = Module.objects.all()
    if module_id != '':
        module = Module.objects.get(id=module_id)
        courses = Course.objects.all().filter(module=module)
        questions = [Question.objects.all().filter(course=course) for course in courses]
        print(len(questions[0]))
        print("hello world", courses, '  ', questions)
        print()
        context = {
            "module": module,
            "courses": [(index, course) for index, course in enumerate(courses)],
            "modules": modules,
            "questions": questions,
        }
        return render(request, "exam/prepare_exam.html", context)
    questions = []

    context = {
        "modules": modules
    }
    return redirect('home')


@login_required(login_url="student:login")
def do_exam(request):
    global arms, ts, STUDENT, MODULE, COURSES
    if request.method == "POST":
        start, courses, nb_questions = request.POST.get("start"),request.POST.getlist("courses[]"),request.POST.get("nb_questions")
        courses = [Course.objects.get(id=course) for course in courses]
        questions = [Question.objects.all().filter(course=course) for course in courses]
        STUDENT = Student.objects.get(user=request.user)
        MODULE = courses[0].module
        COURSES = courses
        qts = [] 
        for question in  questions:
            qts += question
        pprint.pprint(len(qts))
        questions_rewards = [
            StudentQuestions.objects.get_or_create(
                student=Student.objects.get(user=request.user), question=question
            )[0].get_reward()
            for question in qts
        ]
        ts = ThompsonSampler(qts, questions_rewards, int(nb_questions))
        arms = [(index,qts[qts_index].get_question()) for index, qts_index in enumerate(ts.select_arms())]
        context = {
            "is_exam": True,
            "start": start,
            "id": id,
            "questions": arms,
            "all_questions_num":len(arms),
        }
        return render(request, "exam/exam.html", context)
    return HttpResponse("hello world")


@login_required(login_url="student:login")
def result_of_exam(request):
    if request.method == "POST":
        answers = []
        for i in range(len(arms)):
            answers.append(request.POST.getlist(f"answer{i}[]"))
        time = request.POST.getlist("time[]")
        exam:Exam  = ts.update_review(STUDENT, arms, answers, time, MODULE, COURSES)
        context = {
            "id": exam.id,
            "module":exam.module,
            "questions": exam.response_questions,
            "all_questions_num": len(exam.response_questions),
            "time_total": exam.time_taken,
            "date_passed":exam.date_passed,
            "note": exam.note,
            "time_passed": exam.time_passed,
            "nb_correct_answers": exam.num_correct_answers
        }

        # return HttpResponse(
        #     f'{context["id"]}, {context["module"]}, {context["questions"]}, {context["all_questions_num"]}, {context["time_total"]}, {context["date_passed"]}, {context["note"]}, {context["time_passed"]}'
        # )
        #
        return render(request, "exam/result.html", context)
