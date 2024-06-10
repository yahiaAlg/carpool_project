# Generated by Django 5.0.6 on 2024-06-10 18:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('joined_date', models.DateField(auto_now_add=True)),
                ('trips_posted', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('gender', models.CharField(max_length=10)),
                ('age', models.IntegerField()),
                ('trips_taken', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_location', models.CharField(max_length=100)),
                ('to_location', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('meeting_point', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('available_seats', models.IntegerField()),
                ('vehicle_make', models.CharField(max_length=50)),
                ('vehicle_model', models.CharField(max_length=50)),
                ('vehicle_type', models.CharField(max_length=50)),
                ('vehicle_number', models.CharField(max_length=50)),
                ('air_conditioned', models.BooleanField(default=False)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.driver')),
                ('passengers', models.ManyToManyField(related_name='trips', to='pages.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('reported_by', models.CharField(max_length=100)),
                ('date_reported', models.DateField(auto_now_add=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.trip')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=50)),
                ('vehicle_type', models.CharField(max_length=50)),
                ('license_plate', models.CharField(max_length=15)),
                ('air_conditioned', models.BooleanField(default=False)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.driver')),
            ],
        ),
    ]