# Generated by Django 4.2.7 on 2023-11-25 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0009_alter_questions_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='question',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='questions',
            name='topic',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
