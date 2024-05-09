from django.contrib import admin
from exam.models import Exam
class ExamAdmin(admin.ModelAdmin):
    readonly_fields = ("date_passed", "time_passed")


admin.site.register(Exam, ExamAdmin)
# Register your models here.

