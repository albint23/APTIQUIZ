# Generated by Django 4.2.7 on 2023-11-25 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0004_questions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizzes',
            name='difficulty',
        ),
        migrations.AddField(
            model_name='questions',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='quiz_imgs'),
        ),
        migrations.AddField(
            model_name='questions',
            name='topic',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
