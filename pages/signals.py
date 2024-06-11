from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Passenger


@receiver(post_save, sender=User)
def create_passenger_profile(sender, instance, created, **kwargs):
    if created:
        Passenger.objects.create(
            user=instance,
            name=instance.username,
            phone="Not provided",
            gender="Not provided",
            age=0,
            trips_taken=0,
        )
