# Generated by Django 2.1.5 on 2019-01-29 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0005_myuser_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='full_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]