# Generated by Django 5.0.6 on 2024-06-10 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='status',
            field=models.CharField(default='scheduled', max_length=25),
        ),
    ]
