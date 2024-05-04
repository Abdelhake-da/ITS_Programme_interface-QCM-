# Generated by Django 5.0.2 on 2024-04-15 07:02

import django.db.models.deletion
import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=15, max_length=30, prefix='mod-', primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=15, max_length=30, prefix='crs-', primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.module')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=15, max_length=30, prefix='qst-', primary_key=True, serialize=False, unique=True)),
                ('qst_text', models.TextField()),
                ('qst_choices', models.TextField()),
                ('qst_correct_answer', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.course')),
            ],
        ),
    ]
