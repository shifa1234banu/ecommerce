# Generated by Django 3.2 on 2021-06-10 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('week8', '0005_auto_20210610_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='newprice',
            field=models.IntegerField(blank=True),
        ),
    ]
