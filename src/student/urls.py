from django.urls import path
from student import views

app_name = "student"

urlpatterns = [
    path("", views.index,name= "index"),
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
]
