# Generated by Django 5.0.2 on 2024-05-07 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_remove_exam_questions_exam_date_exam_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
