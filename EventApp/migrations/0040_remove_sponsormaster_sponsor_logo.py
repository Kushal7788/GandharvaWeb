# Generated by Django 2.1.1 on 2019-02-13 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0039_auto_20190213_0757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsormaster',
            name='sponsor_logo',
        ),
    ]
