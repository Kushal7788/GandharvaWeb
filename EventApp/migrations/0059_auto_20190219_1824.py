# Generated by Django 2.1.5 on 2019-02-19 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('EventApp', '0058_merge_20190218_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='HearAboutUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, default=None, max_length=200)),
            ],
        ),
        migrations.AlterModelOptions(
            name='roleassignment',
            options={'ordering': ['role']},
        ),
        migrations.AlterModelOptions(
            name='rolemaster',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='myuser',
            name='user_dept',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    to='EventApp.Department'),
        ),
        migrations.AlterUniqueTogether(
            name='assignsub',
            unique_together={('rootuser', 'subuser')},
        ),
        migrations.AddField(
            model_name='hearaboutus',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
