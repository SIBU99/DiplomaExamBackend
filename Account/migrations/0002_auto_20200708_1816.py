# Generated by Django 3.0.8 on 2020-07-08 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='regno',
            field=models.SlugField(max_length=13, primary_key=True, serialize=False, unique=True, verbose_name='Registartion Number'),
        ),
    ]
