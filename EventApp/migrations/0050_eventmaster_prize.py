# Generated by Django 2.1.1 on 2019-02-13 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0049_auto_20190213_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmaster',
            name='prize',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]
