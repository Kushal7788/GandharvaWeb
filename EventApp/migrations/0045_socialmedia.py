# Generated by Django 2.1.1 on 2019-02-13 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0044_department_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('src', models.CharField(max_length=200)),
            ],
        ),
    ]