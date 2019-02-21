# Generated by Django 2.1.1 on 2019-02-19 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('EventApp', '0059_auto_20190219_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmaster',
            name='head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='head', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventmaster',
            name='jt_head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='jt_head', to=settings.AUTH_USER_MODEL),
        ),
    ]
