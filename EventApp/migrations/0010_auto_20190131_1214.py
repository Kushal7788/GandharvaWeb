# Generated by Django 2.1.1 on 2019-01-31 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EventApp', '0009_eventmaster_timings'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstamojoCredential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('token', models.CharField(max_length=50)),
                ('salt', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=50, unique=True)),
                ('transaction_request_id', models.CharField(max_length=50)),
                ('instrment_type', models.CharField(max_length=50)),
                ('billing_instrument', models.CharField(max_length=70)),
                ('status', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='team',
            name='team_name',
        ),
        migrations.AddField(
            model_name='receipt',
            name='name',
            field=models.CharField(max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='prof_img',
            field=models.ImageField(blank=True, upload_to='profile_img'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EventApp.Receipt'),
        ),
    ]