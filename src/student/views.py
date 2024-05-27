import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from app.models import Module
from student.forms import CreateNewUser
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from student import decorators
from algorithms import plots,methods
from algorithms.graph_model import *
from student.models import Student


from openai import OpenAI

# Create your views here.
from django.conf import settings


def index(request):
    modules = Module.objects.all()
    context = {
        "modules": modules,
    }
    # methods.open_ai_api()
    return render(request, "home.html",context=context)
@decorators.notLoggedUsers
def user_login(request):
    # methods.open_ai_api()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("student:index")
        else:
            messages.info(request, 'Username OR password is incorrect')
    return render(request, "student_temp/login.html")


@decorators.notLoggedUsers
def user_signup(request):
    if request.method == "POST":
        form = CreateNewUser(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get('email')
            birth_day = request.POST.get("birth_day")
            phone_number = request.POST.get("phone_number")
            university = request.POST.get("university")
            password = form.cleaned_data.get('password1')
            student = Student.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                birth_day=birth_day,
                phone=phone_number,
                univ=university,
                password=password,
            )[0]
            user = student.user
            # first_name = form.cleaned_data.get
            group = Group.objects.get(name='student')
            user.groups.add(group)
            

            messages.success(request, f'Welcome {user_name}. Your account has been created. You can log in now!')
            return redirect("student:login")
    else:
        form = CreateNewUser()
    context = {
        "form": form
    }

    return render(request, "student_temp/signup.html", context)


def user_logout(request):
    logout(request)
    return redirect("student:login")


@login_required(login_url="student:login")
def user_profile(request):
    student: Student = Student.objects.get(user=request.user)
    exams = Exam.objects.all().filter(student= student)
    print(exams)
    if request.method == "POST":
        try:
            student.img = request.FILES["img"]
        except:
            pass
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.email = request.POST.get("email")
        student.birth_day = datetime.datetime.strptime(
            request.POST.get("birth_day"), "%Y-%m-%d"
        ).date()
        student.address = request.POST.get("address")
        student.country = request.POST.get("county")
        student.city = request.POST.get("city")
        student.about = request.POST.get("about")
        student.phone = request.POST.get("phone")
        student.univ = request.POST.get("univ")
        student.save()
        
    context = {
        "student_module_test_data": student_module_test(student),
        "module_subjects_data":  module_subjects(student),
        "nsc":mean_note_of_course(student),
        "tsc":time_taking_of_course(student),
    }
    return render(request, "student_temp/profile.html",context=context)
