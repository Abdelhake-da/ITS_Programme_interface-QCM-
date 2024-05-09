from django.urls import path
from app import views

app_name = "app"

urlpatterns = [
    path("module-db/", views.db_module, name="module-db"),
    path("add-module/", views.add_module, name="add-module"),
    path("course-db/", views.db_course, name="course-db"),
    path("add-course/", views.add_course, name="add-course"),
    path("question-db/", views.db_question, name="questions-db"),
    path("add-question/", views.add_question, name="add-question"),
    path(
        "import-data-from-json-file/",
        views.import_data_from_json_file,
        name="import-data-from-json-file",
    ),
    path(
        "delete-question/<str:question_id>/",
        views.delete_question,
        name="delete-question",
    ),
]
