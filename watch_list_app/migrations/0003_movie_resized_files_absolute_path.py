# Generated by Django 4.0.5 on 2022-07-06 15:27

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watch_list_app', '0002_movie_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='resized_files_absolute_path',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), null=True, size=None),
        ),
    ]
