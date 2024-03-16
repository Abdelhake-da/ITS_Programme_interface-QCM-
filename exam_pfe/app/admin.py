from django import forms
from django.contrib import admin
from django.contrib.postgres.forms import SimpleArrayField
from . import models

admin.site.register(models.Course)
admin.site.register(models.Module)
admin.site.register(models.CourseFile)
admin.site.register(models.Question)
admin.site.register(models.PossibleChoice)
admin.site.register(models.CorrectAnswer)
admin.site.register(models.Student)
admin.site.register(models.Student_Course_Reward)

