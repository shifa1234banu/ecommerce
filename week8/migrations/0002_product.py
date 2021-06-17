# Generated by Django 3.2 on 2021-06-04 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('week8', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image1', models.ImageField(upload_to='photos/productimages')),
                ('image2', models.ImageField(upload_to='photos/productimages')),
                ('image3', models.ImageField(blank=True, upload_to='photos/productimages')),
                ('image4', models.ImageField(blank=True, upload_to='photos/productimages')),
                ('brand', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('offers', models.IntegerField()),
                ('size', models.CharField(choices=[('xs', 'XS'), ('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL')], default='s', max_length=6)),
                ('stock', models.IntegerField()),
            ],
        ),
    ]
