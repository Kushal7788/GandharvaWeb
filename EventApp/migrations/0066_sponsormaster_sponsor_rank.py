# Generated by Django 2.1.1 on 2019-02-20 11:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('EventApp', '0065_auto_20190220_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsormaster',
            name='sponsor_rank',
            field=models.IntegerField(default=1),
        ),
    ]
