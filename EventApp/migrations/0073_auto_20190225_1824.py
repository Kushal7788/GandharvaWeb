# Generated by Django 2.1.5 on 2019-02-25 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0072_auto_20190225_0000'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsorCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor_category', models.CharField(max_length=30)),
                ('category_rank', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='sponsormaster',
            name='sponsor_category',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='EventApp.SponsorCategory'),
        ),
    ]
