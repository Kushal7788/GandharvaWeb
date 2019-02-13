# Generated by Django 2.1.5 on 2019-02-11 15:17

import EventApp.models
import EventApp.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0027_instamojocredential_redirect_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedocument',
            name='document',
            field=models.FileField(upload_to=EventApp.models.filePath, validators=[EventApp.validators.validate_file_size]),
        ),
    ]
