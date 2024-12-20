# Generated by Django 4.2.7 on 2023-11-22 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0003_alter_quizzes_difficulty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, null=True)),
                ('option_1', models.CharField(max_length=100, null=True)),
                ('option_2', models.CharField(max_length=100, null=True)),
                ('option_3', models.CharField(max_length=100, null=True)),
                ('option_4', models.CharField(max_length=100, null=True)),
                ('answer', models.CharField(max_length=100, null=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.quizzes')),
            ],
        ),
    ]
