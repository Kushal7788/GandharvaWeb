# Generated by Django 2.1.1 on 2019-01-31 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0010_auto_20190131_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='prof_img',
            field=models.ImageField(blank=True, height_field=200, upload_to='profile_img/%Y/%m/%d/', width_field=200),
        ),
    ]