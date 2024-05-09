# Generated by Django 5.0.2 on 2024-05-07 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='questions',
        ),
        migrations.AddField(
            model_name='exam',
            name='date',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='time',
            field=models.TimeField(auto_now=True, null=True),
        ),
    ]
