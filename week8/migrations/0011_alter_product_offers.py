# Generated by Django 3.2 on 2021-07-08 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('week8', '0010_alter_category_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='offers',
            field=models.CharField(default=0, max_length=2),
        ),
    ]
