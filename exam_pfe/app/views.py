import random
from django.shortcuts import render

from .models import Student
from .data import questions
from .classes.thompson_sampler import ThompsonSampler

student = Student(name="Abdelhake")
sampler = ThompsonSampler(questions)

def home(request):
    context = {
        "student": student,
        "get_questions": None,
    }
    return render(request, "index.html",context=context)

def is_correct(answer, correct_answer):
    if len(answer) != len(correct_answer):
        return False
    else:
        print("hello")
        for i in range(len(answer)):
            if int(answer[i]) not in correct_answer:
                return False
        return True
def solution(question):
    strs =  "Oops, your answer was incorrect. The correct answer is:"
    for i in question["correct_answer"]: 
       strs += str(question["possible_choses"][i - 1][0])
    return strs    
def index(request):
    if request.method == "POST":
        time_taken = float(request.POST.get("time"))
        answer = request.POST.getlist("answer[]")
        correct_answer = questions[int(request.POST.get("arm"))]["correct_answer"]
        success = is_correct(answer, correct_answer)
        sampler.update(int(request.POST.get("arm")), success, time_taken)

        feedback = (
            [0, "You answered correctly!"]
            if success
            else [
                1,
                solution(questions[int(request.POST.get("arm"))])
            ]
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
            "index_copy.html",
            {
                "question": question,
                "possible_choses": random.sample(possible_choses, len(possible_choses)),
                "arm": arm,
                "feedback": feedback,
                "results": results,
            },
        )
    else:
        arm = sampler.select_arm()
        question = questions[arm]["question"]
        possible_choses = questions[arm]["possible_choses"]
        return render(
            request,
            "index_copy.html",
            {
                "question": question,
                "possible_choses": random.sample(possible_choses, len(possible_choses)),
                "arm": arm,
                "feedback": [0, ""],
            },
        )
