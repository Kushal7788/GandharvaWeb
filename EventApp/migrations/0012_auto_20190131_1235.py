# Generated by Django 2.1.1 on 2019-01-31 12:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('EventApp', '0011_auto_20190131_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='prof_img',
            field=models.ImageField(blank=True, upload_to='profile_img/%Y/%m/%d/'),
        ),
    ]
