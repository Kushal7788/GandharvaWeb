# Generated by Django 2.1.1 on 2019-01-30 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0007_merge_20190129_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmaster',
            name='location',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
