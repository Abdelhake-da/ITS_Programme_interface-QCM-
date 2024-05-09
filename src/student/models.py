from django.db import models
import numpy as np
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import User
from app.models import Course

class Student(models.Model):
    user = models.OneToOneField(User, null=True ,on_delete=models.CASCADE)
    id = ShortUUIDField(
        unique=True,
        length=15,
        max_length=30,
        prefix="student-",
        alphabet="abcdefgh12345",
        primary_key=True,
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_day = models.DateField(null=True)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    register_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    courses_exams = models.ManyToManyField(Course)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
class StudentQuestions(models.Model) :

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.reward:
            self.reward = self.get_start_reward()

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey('app.Question', on_delete=models.CASCADE)
    successes = models.IntegerField(default=0)
    failures = models.IntegerField(default=0)
    successes_time = models.FloatField(default=0, null=True, blank=True, max_length=100)
    successes_time_index = models.JSONField(default=list, null=True, blank=True)
    time_taking = models.JSONField(default=list, null=True, blank=True)
    reward = models.FloatField(max_length=100)

    def __str__(self):
        return f'{self.student.user} - {self.question.qst_text}'
    def get_reward(self):
        return self.reward
    def get_start_reward(self):
        return 4 + (np.random.rand() / 5)
