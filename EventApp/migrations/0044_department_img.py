# Generated by Django 2.1.1 on 2019-02-13 08:47

import EventApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0043_remove_department_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='img',
            field=models.ImageField(blank=True, upload_to=EventApp.models.department_path),
        ),
    ]
