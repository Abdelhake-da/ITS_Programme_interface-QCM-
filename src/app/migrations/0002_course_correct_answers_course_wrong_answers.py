# Generated by Django 5.0.2 on 2024-05-13 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='correct_answers',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='wrong_answers',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
