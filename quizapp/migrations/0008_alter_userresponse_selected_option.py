# Generated by Django 4.2.7 on 2023-11-25 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0007_userresponse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userresponse',
            name='selected_option',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]