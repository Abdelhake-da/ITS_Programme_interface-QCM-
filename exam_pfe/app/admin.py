from django.contrib import admin

from .models import Lesson, QuestionExam, QuestionReward, Student, Subject

# Register your models here.
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(QuestionExam)
admin.site.register(Student)
admin.site.register(QuestionReward)