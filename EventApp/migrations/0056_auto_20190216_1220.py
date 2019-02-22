# Generated by Django 2.1.5 on 2019-02-16 06:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('EventApp', '0055_auto_20190216_1218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='description',
            new_name='descriptionfg',
        ),
        migrations.RemoveField(
            model_name='department',
            name='rank1fg',
        ),
        migrations.AddField(
            model_name='department',
            name='rank',
            field=models.IntegerField(default=1),
        ),
    ]
