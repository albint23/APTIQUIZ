# Generated by Django 4.2.7 on 2023-12-29 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0016_quizzes_attendees'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizzes',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
