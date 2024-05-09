# Generated by Django 5.0.2 on 2024-05-07 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_remove_exam_date_remove_exam_time_exam_date_passed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='num_correct_answers',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='time_passed',
            field=models.TimeField(auto_now_add=True),
        ),
    ]