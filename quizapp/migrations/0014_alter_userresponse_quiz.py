# Generated by Django 4.2.7 on 2023-12-28 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0013_userresponse_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userresponse',
            name='quiz',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='quizapp.quizzes'),
        ),
    ]
