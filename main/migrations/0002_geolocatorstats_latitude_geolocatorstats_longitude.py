# Generated by Django 5.0.1 on 2024-02-11 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='geolocatorstats',
            name='latitude',
            field=models.DecimalField(decimal_places=20, default=0, max_digits=30),
        ),
        migrations.AddField(
            model_name='geolocatorstats',
            name='longitude',
            field=models.DecimalField(decimal_places=20, default=0, max_digits=30),
        ),
    ]