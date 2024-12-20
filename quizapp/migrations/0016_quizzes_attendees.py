# Generated by Django 4.2.7 on 2023-12-28 08:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizapp', '0015_alter_userresponse_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizzes',
            name='attendees',
            field=models.ManyToManyField(blank=True, related_name='attended_quizzes', to=settings.AUTH_USER_MODEL),
        ),
    ]
