# Generated by Django 2.1.1 on 2019-02-06 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0017_auto_20190205_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
