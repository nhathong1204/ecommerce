# Generated by Django 3.2 on 2023-12-23 15:17

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20231223_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='cover_image',
            field=models.ImageField(default='vendor.jpg', upload_to=core.models.user_directory_path),
        ),
    ]
