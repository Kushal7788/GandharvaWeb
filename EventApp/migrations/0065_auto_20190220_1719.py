# Generated by Django 2.1.1 on 2019-02-20 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0064_sponsormaster_sponsor_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventmaster',
            name='head',
        ),
        migrations.RemoveField(
            model_name='eventmaster',
            name='jt_head',
        ),
    ]
