# Generated by Django 2.1.1 on 2019-02-13 08:09

import EventApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0040_remove_sponsormaster_sponsor_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsormaster',
            name='sponsor_logo',
            field=models.ImageField(blank=True, upload_to=EventApp.models.sponsor_path),
        ),
    ]