# Generated by Django 3.2 on 2021-06-13 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zehak', '0004_auto_20210611_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='otp',
        ),
        migrations.AddField(
            model_name='profile',
            name='num',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
    ]
