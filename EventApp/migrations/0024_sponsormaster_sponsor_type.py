# Generated by Django 2.1.5 on 2019-01-22 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0023_college'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsormaster',
            name='sponsor_type',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]