import json
import pprint
from typing import List
from django.http import HttpResponse
from django.shortcuts import redirect, render
from app.models import Course, Module, Question
from app.forms import CourseForm, ModuleForm, QuestionForm
from student import decorators
from django.contrib.auth.decorators import login_required

@login_required(login_url="student:login")
@decorators.allowedUsers(allowedUsers=["admin"])
def db_module(request):
    modules: List[Module] = Module.objects.all()

    context = {
        "modules": [ module.get_module() for module in modules],
        'form'  :ModuleForm()
    }
    return render(request, "app_temp/add_module.html",context=context)


@login_required(login_url="student:login")
@decorators.allowedUsers(allowedUsers=["admin"])
def add_module(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module_name = form.cleaned_data['module_name']
            module = Module.objects.get_or_create(name=module_name)[0]
            module.save()
            return redirect("module-db")
    else:
        form = ModuleForm()
    return redirect("module-db")


@login_required(login_url="student:login")
@decorators.allowedUsers(allowedUsers=["admin"])
def db_course(request):
    courses: List[Course] = Course.objects.all()
    context = {
        "courses": [course.get_course() for course in courses],
        "form": CourseForm(),
    }
    return render(request, "app_temp/add_course.html", context=context)


@login_required(login_url="student:login")
@decorators.allowedUsers(allowedUsers=["admin"])
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            module = Module.objects.get(id=form.cleaned_data["module"])
            course_name = form.cleaned_data["course_name"]
            course = Course.objects.get_or_create(name=course_name, module=module)[0]
            course.save()
            return redirect("course-db")
    else:
        form = CourseForm()
    return redirect("course-db")


@login_required(login_url="student:login")
@decorators.allowedUsers(allowedUsers=["admin"])
def db_question(request):
    questions: List[Question] = Question.objects.all()
    context = {
        "questions": [question.get_question() for question in questions],
        "form": QuestionForm(),
    }
    return render(request, "app_temp/add_question.html", context=context)


@login_required(login_url="student:login")
@decorators.allowedUsers(allowedUsers=["admin"])
def add_question(request):
    if request.method == "POST":

        form = QuestionForm(request.POST)
        if form.is_valid():
            course = Course.objects.get(id=form.cleaned_data["course"])
            question_text:str = form.cleaned_data["question_text"]
            choices:list = request.POST.getlist("choices[]")
            correct:list =[index for index, value in enumerate(request.POST.getlist("is_correct[]")) if bool(int(value)) ] 
            type_post = request.POST.get('type')
            if  len(choices) != 0 and len(correct) != [] :
                if type_post == "add":
                    question: Question = Question.objects.get_or_create(
                        course=course,
                        qst_text=question_text,
                        qst_choices="\n".join(choices),
                        qst_correct_answer="\n".join(str(item) for item in correct),
                    )[0]
                    question.save()
                else:
                    question: Question = Question.objects.get(id = type_post)
                    question.update_questions(
                        course,
                        question_text,
                        "\n".join(choices),
                        "\n".join(str(item) for item in correct),
                    )
                    question.save()
            return redirect("questions-db")
    else:
        form = QuestionForm()
    return redirect("questions-db")


@login_required(login_url="student:login")
@decorators.allowedUsers(allowedUsers=["admin"])
def import_data_from_json_file (request):
    # loop through the data and create the objects
    with open("app/data1.json", "r") as f:
        data = json.load(f)
    for module in data:
        module_name = module["module"]
        model_module = Module.objects.get_or_create(name = module_name)[0]
        for course in module["courses"]:
            course_name = course["course"]
            model_course = Course.objects.get_or_create(name = course_name, module = model_module)[0]
            for question in course["questions"]:
                question_text = question["question"]
                choices = "\n".join(str(item) for item in question["choices"])
                answers = "\n".join(str(item) for item in question["answers"])
                question = Question.objects.get_or_create(
                    qst_text = question_text,
                    qst_choices = choices,
                    qst_correct_answer = answers,
                    course = model_course
                )
    return HttpResponse("done")


@login_required(login_url="student:login")
@decorators.allowedUsers(allowedUsers=["admin"])
def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    return redirect("questions-db")
