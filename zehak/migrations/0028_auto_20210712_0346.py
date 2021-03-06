# Generated by Django 3.2 on 2021-07-11 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zehak', '0027_auto_20210712_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Failed', 'Failed'), ('Success', 'Success')], default='Success', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Returned', 'Returned'), ('Placed', 'Placed'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled')], default='Placed', max_length=20),
        ),
    ]
