# Generated by Django 2.1.1 on 2019-01-27 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0028_auto_20190127_1838'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documents',
            options={'ordering': ['category']},
        ),
    ]
