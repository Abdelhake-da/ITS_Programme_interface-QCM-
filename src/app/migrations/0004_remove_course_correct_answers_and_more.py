# Generated by Django 5.0.2 on 2024-05-15 03:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_course_wrong_answers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='correct_answers',
        ),
        migrations.RemoveField(
            model_name='course',
            name='wrong_answers',
        ),
    ]
