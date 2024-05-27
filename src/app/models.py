import random
from django.db import models
from shortuuid.django_fields import ShortUUIDField


class Module(models.Model):
    id = ShortUUIDField(
        unique=True, length=15, max_length=30, prefix="mod-", alphabet="abcdefgh12345",primary_key=True
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    def get_module(self):
        return {"id": self.id, "name": self.name}


class Course(models.Model):
    id = ShortUUIDField(
        unique=True,
        length=15,
        max_length=30,
        prefix="crs-",
        alphabet="abcdefgh12345",
        primary_key=True,
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
   
    def __str__(self):
        return self.name
    def get_course(self):
        return {
            'id':self.id,
            'name':self.name,
            'module':self.module
        }


class Question(models.Model):
    id = ShortUUIDField(
        unique=True,
        length=15,
        max_length=30,
        prefix="qst-",
        alphabet="abcdefgh12345",
        primary_key=True,
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    qst_text = models.TextField()
    qst_choices = models.TextField()
    qst_correct_answer = models.TextField()

    def __str__(self):
        return f"{self.qst_text}"
    def get_choices(self):
        return [ (index, choice) for index, choice in enumerate(self.qst_choices.replace("\r","").split('\n'))]
    def get_correct_answer(self):
        return self.qst_correct_answer.replace("\r", "").split("\n")
    def get_question(self):
        choices = self.get_choices()
        random.shuffle(choices)
        return {
            "id": self.id,
            "qst_text": self.qst_text,
            "qst_choices": choices,
            "qst_correct_answer": self.get_correct_answer(),
            "course": self.course.get_course(),
        }
    def update_questions(self, course, qst_text, qst_choices, qst_correct_answer):
        self.course = course
        self.qst_text = qst_text
        self.qst_choices = qst_choices
        self.qst_correct_answer = qst_correct_answer
