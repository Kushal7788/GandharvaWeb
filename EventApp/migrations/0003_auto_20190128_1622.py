# Generated by Django 2.1.1 on 2019-01-28 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0002_college_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='user_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='EventApp.College_year'),
        ),
    ]