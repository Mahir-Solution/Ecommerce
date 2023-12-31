# Generated by Django 4.2.3 on 2023-09-16 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Category', '0002_alter_category_model_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('product_image', models.ImageField(upload_to='image')),
                ('description', models.TextField(blank=True)),
                ('price', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('is_available', models.BooleanField(default=True)),
                ('cteated_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
                ('catgoryfk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Category.category_model')),
            ],
        ),
    ]
