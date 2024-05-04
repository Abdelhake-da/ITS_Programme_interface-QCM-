import pprint
from typing import List
from django.http import HttpResponse
from django.shortcuts import render
from app.models import Course, Module, Question
from student.models import StudentQuestions, Student
from algorithms.thompson_sampler import ThompsonSampler
# Create your views here.
arms = []
ts: ThompsonSampler = None
def index(request):
    return render(request, "index.html")
def prepare_exam(request, module_id=''):
    
    modules = Module.objects.all()
    if module_id != '':
        module = Module.objects.get(id=module_id)
        courses = Course.objects.all().filter(module=module)
        questions = [Question.objects.all().filter(course=course) for course in courses]
        print(len(questions[0]))
        print("hello world ", courses, '  ', questions)
        print()
        context = {
            "module": module,
            "courses": [(index, course) for index, course in enumerate(courses)],
            "modules": modules,
            "questions": questions,
        }
        return render(request, "index.html", context)
    questions = []

    context = {
        "modules": modules
    }
    return render(request, "index.html", context)


def do_exam(request):
    global arms, ts
    if request.method == "POST":
        start, id, courses, nb_questions = request.POST.get("start"),request.POST.get("id"),request.POST.getlist("courses[]"),request.POST.get("nb_questions")
        courses = [Course.objects.get(id=course) for course in courses]
        questions = [Question.objects.all().filter(course=course) for course in courses]
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
            "exam": True,
            "start": start,
            "id": id,
            "questions": arms,
            "all_questions_num":len(arms),
        }
        return render(request, "index.html", context)
    return HttpResponse("hello world")
def result_of_exam(request):
    if request.method == "POST":
        answers = []
        for i in range(len(arms)):
            answers.append(request.POST.getlist(f"answer{i}[]"))
        time = request.POST.getlist("time[]")
        ts.update_review(Student.objects.get(user = request.user), arms, answers, time)
        context = {
            "response": True,
            "id": id,
            "questions": arms,
            "all_questions_num":len(arms),
            "answers": answers,
            "time": time
        }
        return render(request, "index.html", context)
    return HttpResponse("hello world")
