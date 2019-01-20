# Generated by Django 2.1.5 on 2019-01-19 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0014_remove_eventmaster_under_which_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventmaster',
            name='round1',
        ),
        migrations.RemoveField(
            model_name='eventmaster',
            name='round2',
        ),
        migrations.AddField(
            model_name='eventmaster',
            name='rounds',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='eventmaster',
            name='objective',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='eventmaster',
            name='rules',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]