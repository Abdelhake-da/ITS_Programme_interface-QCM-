import datetime
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from app.models import Course,Module,Question
from student.models import Student
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Exam(models.Model):
    id = ShortUUIDField(
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
    response_questions = models.TextField(default='') 
    time_taken = models.FloatField(default=0)
    note = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    date_passed = models.DateField(auto_now_add=True)
    time_passed = models.TimeField(auto_now_add=True)
    num_correct_answers = models.IntegerField(null=True)

