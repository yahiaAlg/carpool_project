# Generated by Django 5.0.6 on 2024-06-10 21:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_remove_trip_time_alter_trip_date_alter_trip_driver_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='driver_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='passenger_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
