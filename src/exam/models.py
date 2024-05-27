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
    def __str__(self):
        return f"{self.student}    {self.id}"

class Subject_answers_for_student(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,blank=True)
    correct_answers = models.IntegerField(blank=True, default=0, null=True)
    wrong_answers = models.IntegerField(blank=True,default=0,null=True)
    time_taking = models.FloatField(blank=True, null=True, default=0)
    def __str__(self):
        return f"{self.student} -- {self.course}"
