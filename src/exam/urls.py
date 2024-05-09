from django.urls import path
from exam import views

app_name = "exam"

urlpatterns = [
    path("", views.index, name="index"),
    path("prepare-exam/", views.prepare_exam, name="prepare"),
    path("prepare-exam/<str:module_id>/", views.prepare_exam, name="prepare-exam"),
    path("do-exam/", views.do_exam, name="do-exam"),
    path("result/", views.result_of_exam, name="result"),
]
