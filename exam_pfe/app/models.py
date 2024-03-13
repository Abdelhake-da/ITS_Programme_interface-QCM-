from django.db import models


class Module(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    COURSE_QUESTION_TYPES = (
        ("qcm", "Multiple Choice"),
        ("one_word", "One Word Response"),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=10, choices=COURSE_QUESTION_TYPES)
    text = models.TextField()

    def __str__(self):
        return self.text


class CourseFile(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to="course_files/")

    def __str__(self):
        return str(self.file)


class PossibleChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    choice_value = models.IntegerField()

    def __str__(self):
        return self.choice_text


class CorrectAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_value = models.IntegerField()

    def __str__(self):
        return str(self.answer_value)
