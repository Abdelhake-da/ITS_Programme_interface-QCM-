from django.db import models
from shortuuid.django_fields import ShortUUIDField
from app.models import Course,Module,Question
from student.models import Student

# Create your models here.
class Exam(models.Model):
    id = id = ShortUUIDField(
        unique=True,
        length=15,
        max_length=30,
        prefix="exam-",
        alphabet="abcdefghijklmnopqrstuvwxyz123456789",
        primary_key=True,
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    courses =  models.ManyToManyField(Course)
    
