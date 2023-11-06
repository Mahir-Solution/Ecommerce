# Generated by Django 4.2.3 on 2023-10-26 04:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Cart', '0002_cartitem_model_variationfk'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem_model',
            name='registrationfk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
