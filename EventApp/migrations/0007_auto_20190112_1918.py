# Generated by Django 2.1.1 on 2019-01-12 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0006_auto_20190112_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventmaster',
            name='rules',
            field=models.CharField(max_length=300),
        ),
    ]