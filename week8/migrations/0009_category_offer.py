# Generated by Django 3.2 on 2021-07-06 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('week8', '0008_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='offer',
            field=models.IntegerField(default=0),
        ),
    ]
