# Generated by Django 2.1.5 on 2019-01-31 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0012_auto_20190131_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(max_length=100),
        ),
    ]
