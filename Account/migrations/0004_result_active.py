# Generated by Django 3.0.8 on 2020-07-10 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0003_auto_20200708_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='active',
            field=models.BooleanField(default=False, help_text='Student will be alowed to enter the exam and also allow to submit the exam', verbose_name='Active'),
        ),
    ]