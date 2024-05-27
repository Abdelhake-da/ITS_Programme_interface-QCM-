from django.contrib import admin
from exam.models import Exam, Subject_answers_for_student
class ExamAdmin(admin.ModelAdmin):
    readonly_fields = ("date_passed", "time_passed")


admin.site.register(Exam, ExamAdmin)
admin.site.register(Subject_answers_for_student)
# Register your models here.

