# Generated by Django 4.2.3 on 2023-09-14 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category_model',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]