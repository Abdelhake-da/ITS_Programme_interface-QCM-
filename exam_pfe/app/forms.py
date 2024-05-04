from django import forms
from app.models import Course, Module


# Create your forms here.

class ModuleForm(forms.Form):
    module_name = forms.CharField(
        label="Module name",
        widget=forms.TextInput(
            attrs={"placeholder": "Module name", "id": "name-module"}
        ),
        required=True,
    )


class CourseForm(forms.Form):
    pass
    # module = forms.ChoiceField(
    #     choices=[(module.get_module()['id'],module.get_module()["name"]) for module in Module.objects.all()],
    #     required=True,
    # )
    # course_name = forms.CharField(
    #     max_length=100, widget=forms.TextInput(attrs={"placeholder": "Course Name"})
    # )
class QuestionForm(forms.Form):
    pass
    # course = forms.ChoiceField(
    #     choices=[(course.get_course()['id'],course.get_course()["name"]) for course in Course.objects.all()],
    #     required=True
    # )
    # question_text = forms.CharField(
    #     max_length=500, widget=forms.TextInput(attrs={"placeholder": "Course Name"})
    # )
