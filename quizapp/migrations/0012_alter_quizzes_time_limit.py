# Generated by Django 4.2.7 on 2023-12-27 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0011_quizzes_time_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizzes',
            name='time_limit',
            field=models.FloatField(default=0),
        ),
    ]