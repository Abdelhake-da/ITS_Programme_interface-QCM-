import random
from django.http import HttpResponse
from django.shortcuts import render
# from .data import questions2 as questions
import json
from .models import Module, Course, Question, PossibleChoice, CorrectAnswer


# from .data import questions
from .classes.thompson_sampler import ThompsonSampler
from .classes.q_learning import Q_learning


def get_data_from_db(module, course, type):
    module_model = Module.objects.get(name=module)
    course_model = Course.objects.get(name=course, module=module_model)
    questions = Question.objects.filter(course=course_model,question_type=type)
    questions_list = []
    for question in questions:
        questions_list.append(
            {
                "question": question.text,
                "possible_choses": list(
                    PossibleChoice.objects.filter(question=question).values_list(
                        "choice_text", "choice_value"
                    ),
                ),
                "correct_answer": list(
                    CorrectAnswer.objects.filter(question=question).values_list(
                        "answer_value", flat=True
                    )
                ),
            }
        )

    return questions_list
def home(request):
    context = {
        "get_questions": None,
    }
    return render(request, "index.html",context=context)

def is_correct(answer, correct_answer):
    if len(answer) != len(correct_answer):
        return False
    else:
        for i in range(len(answer)):
            if int(answer[i]) not in correct_answer:
                return False
        return True


def solution(question):
    strs =  "Oops, your answer was incorrect. The correct answer is:"
    for i in question["correct_answer"]: 
       strs += str(question["possible_choses"][i - 1][0])
    return strs    
def get_courses():
    modules = list(Module.objects.filter())
    courses = {}
    for module in modules:
        courses[module.name] = []
        for course in list(Course.objects.filter(module=module)):
            courses[module.name].append(course.name)
    return courses
questions = None
sampler = None
def prepare_exam_thompson(request, module_name, course_name):
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
    else:
        questions = get_data_from_db(module_name, course_name, "qcm")
        sampler = ThompsonSampler(questions)
        arm = sampler.select_arm()
        question = questions[arm]["question"]
        possible_choses = questions[arm]["possible_choses"]
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


def prepare_exam_q_learning(request, module_name, course_name):
    global questions, sampler

    if request.method == "POST":
        time_taken = float(request.POST.get("time"))
        answer = request.POST.getlist("answer[]")
        correct_answer = questions[int(request.POST.get("arm"))]["correct_answer"]
        success = is_correct(answer, correct_answer)
        sampler.update(
            int(request.POST.get("arm")),
            sampler.get_reward(success, int(request.POST.get("arm")), time_taken),
        )

        feedback = (
            [0, "You answered correctly!"]
            if success
            else [1, solution(questions[int(request.POST.get("arm"))])]
        )
        arm = sampler.select_action(int(request.POST.get("arm")))
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
    else:
        questions = get_data_from_db(module_name, course_name, "qcm")
        sampler = Q_learning(questions)
        arm = sampler.select_action()
        question = questions[arm]["question"]
        possible_choses = questions[arm]["possible_choses"]
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

def index(request):
    return render(
        request,
        "index_copy.html",
        {
            "courses": get_courses(),
        },
    )


def courses(request, module_name, course_name):
    return HttpResponse(course_name)


def module(request, module_name):
    return HttpResponse(module_name)


def upload_json_file(request):
    with open("/home/mr-abdelhake/Documents/projetFE/ITS_Programme_interface(QCM)/exam_pfe/app/data.json", "r") as file:
        data = json.load(file)
        for module in data:
            module_name = module["module"]
            module_model = Module.objects.get_or_create(name=module_name)
            for course in module["course"]:
                course_name = course["cours"]
                course_model = Course.objects.get_or_create(name=course_name, module = module_model[0])

                if len(course["type"]["qcm"]) > 1:
                    questions = course["type"]["qcm"]
                    for question in questions:
                        qcm_txt = question["question"]
                        question_model = Question.objects.get_or_create(
                            text=qcm_txt, course=course_model[0],question_type="qcm"
                        )
                        qcm_choices = question["choices"]
                        for choice in qcm_choices:
                            choice_text = choice["text"]
                            choice_value = int(choice["value"])
                            PossibleChoice.objects.get_or_create(
                                choice_text=choice_text,
                                choice_value=choice_value,
                                question=question_model[0],
                            )
                        qcm_answers = question["answers"]
                        for answer in qcm_answers:
                            try:
                                CorrectAnswer.objects.get_or_create(
                                    answer_value=answer, question=question_model[0]
                                )
                            except:
                                print(
                                    CorrectAnswer.objects.filter(
                                        question=question_model[0], answer_value=answer
                                    )
                                )
                if len(course["type"]["not qcm"]) > 1:
                    questions = course["type"]["not qcm"]
                    for question in questions:
                        not_qcm_txt = question["question"]
                        not_qcm_answers = question["answers"]
                        question_model = Question.objects.get_or_create(
                            text=not_qcm_txt,
                            course=course_model[0],
                            question_type="one_word",
                        )
                        CorrectAnswer.objects.get_or_create(
                            answer_value=not_qcm_answers, question=question_model[0]
                        )

    return HttpResponse("done")
