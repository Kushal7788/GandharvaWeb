# Generated by Django 2.1.1 on 2019-02-13 07:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('EventApp', '0037_auto_20190213_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carousel',
            name='src',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
