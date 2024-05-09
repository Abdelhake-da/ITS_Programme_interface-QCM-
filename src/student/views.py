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
from exam.models import Exam
# Create your views here.

def index(request):
    modules = Module.objects.all()
    context = {
        "modules": modules,
    }
    return render(request, "home.html",context=context)
@decorators.notLoggedUsers
def user_login(request):
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
            user = form.save()
            user_name = form.cleaned_data.get('username')
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
