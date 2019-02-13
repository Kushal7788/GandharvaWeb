# Generated by Django 2.1.5 on 2019-02-13 06:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0036_auto_20190212_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventdepartment',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EventApp.Department'),
        ),
        migrations.AlterField(
            model_name='roleassignment',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
