# Generated by Django 2.1.5 on 2019-02-10 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0026_auto_20190210_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='instamojocredential',
            name='redirect_url',
            field=models.CharField(max_length=60, null=True),
        ),
    ]