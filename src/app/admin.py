from django.contrib import admin
from app import models

admin.site.register(models.Module)
admin.site.register(models.Course)
admin.site.register(models.Question)
