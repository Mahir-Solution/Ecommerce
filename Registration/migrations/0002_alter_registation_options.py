# Generated by Django 4.2.3 on 2023-10-24 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registation',
            options={'permissions': [('can_delete_user', 'Can delete user')]},
        ),
    ]