# Generated by Django 2.1.1 on 2019-02-05 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0016_auto_20190205_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='Refral_Code',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='team',
            name='referral',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Refral_Volunteer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='participant', to=settings.AUTH_USER_MODEL),
        ),
    ]
