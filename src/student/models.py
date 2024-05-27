import os
from django.db import models
import numpy as np
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import User
from app.models import Course, Module
from django.core.validators import RegexValidator
from exam_pfe.settings import BASE_DIR
def upload_img(instance, filename):
    # Get the original file extension
    ext = filename.split(".")[-1]

    # Generate a new filename
    new_filename = f"{instance.id}.{ext}"
    print(os.path.join("images/students/", new_filename))
    # Return the new filename
    return os.path.join("images/students/", new_filename)

date_validator = RegexValidator(
    regex=r"^\d{4}-\d{2}-\d{2}$",
    message='Enter a valid date in the format "YYYY-MM-DD".',
)

class Student(models.Model):
    user = models.OneToOneField(User, null=True,blank=True ,on_delete=models.CASCADE)
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
    email = models.CharField(max_length=100, null=True, blank=True)
    birth_day = models.DateField(null=True, validators=[date_validator],blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(blank=True, max_length=100)
    city = models.CharField(blank=True,max_length=100)
    about = models.TextField(max_length=1000,blank=True,null=True)

    phone = models.CharField(max_length=100, null=True, blank=True)
    univ = models.CharField(max_length=100,blank= True ,null=True)

    module_exams = models.ManyToManyField(Module, blank=True)
    courses_exams = models.ManyToManyField(Course , blank=True)
    img = models.ImageField(
        upload_to=upload_img,
        blank=True,
        default="images/students/user.png",
    )
    password = models.CharField(max_length=100,blank=True,null=True)
    register_date = models.DateTimeField(auto_now_add=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, blank=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if self._state.adding:
            user = User.objects.create_user(
                username=self.id,
                email=self.email,
                first_name=self.first_name,
                last_name=self.last_name,  # You can set a password here or generate one automatically
            )
            user.set_password(
                self.password,
            )
            user.save()

            # Set the student_user foreign key on the Student self to the newly created User self
            self.user = user
            self.password = user.password
            super().save(*args, **kwargs)
        else:
            if "pbkdf2_sha256$720000$" not in self.password:
                self.user.set_password(self.password)
                self.password = self.user.password
            super().save(*args, **kwargs)

    def get_date(self):
        return self.birth_day.strftime("%Y-%m-%d")
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
