# Generated by Django 2.1.1 on 2019-02-13 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0045_socialmedia'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialmedia',
            name='cls',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]