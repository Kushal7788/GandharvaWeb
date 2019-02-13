# Generated by Django 2.1.1 on 2019-02-05 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('EventApp', '0015_auto_20190201_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='EventApp.College')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='referral',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
