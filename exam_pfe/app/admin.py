from django.contrib import admin
from . import models

admin.site.register(models.Course)
admin.site.register(models.Module)
admin.site.register(models.CourseFile)
admin.site.register(models.Question)
admin.site.register(models.PossibleChoice)
admin.site.register(models.CorrectAnswer)
