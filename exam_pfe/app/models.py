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
    # text = models.TextField()
    question = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.course.name} - {self.question_type}"


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
    answer_value = models.CharField(max_length=90)

    def __str__(self):
        return str(self.answer_value)


class Student(models.Model):
    student_id = models.IntegerField()
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student_Course_Reward(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    questions_reward = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"{str(self.student)}_{str(self.course)}"
