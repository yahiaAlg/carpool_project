from django.contrib.auth.models import User
from django.db import models


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    joined_date = models.DateField(auto_now_add=True)
    trips_posted = models.PositiveIntegerField(default=0)


class Vehicle(models.Model):
    make = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=15)
    air_conditioned = models.BooleanField(default=False)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)


class Passenger(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    trips_taken = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Trip(models.Model):
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=25, default="scheduled")
    meeting_point = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available_seats = models.IntegerField()
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=50)
    air_conditioned = models.BooleanField(default=False)
    passengers = models.ManyToManyField(Passenger, related_name="trips")

    def __str__(self):
        return f"{self.from_location} to {self.to_location} on {self.date}"


class Report(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    content = models.TextField()
    reported_by = models.CharField(max_length=100)
    date_reported = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Report for trip {self.trip.id} by {self.reported_by}" # type: ignore
