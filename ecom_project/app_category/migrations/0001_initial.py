# Generated by Django 4.1.2 on 2023-01-07 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('slug', models.CharField(max_length=100, unique=True)),
                ('category_image', models.ImageField(blank=True, upload_to='photos/categories')),
            ],
            options={
                'verbose_name': 'Category Class',
                'verbose_name_plural': 'Category Class',
            },
        ),
    ]