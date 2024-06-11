from django.contrib.auth.models import User
from django.db import models


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=15)
    air_conditioned = models.BooleanField(default=False)
    maker = models.CharField(max_length=50)
    model = models.CharField(max_length=50, default="Not Specified")
    series = models.CharField(max_length=50, default="Not Specified", blank=True)
    type = models.CharField(max_length=50, default="Not Specified")
    max_seats = models.IntegerField(default=4)

    def __str__(self) -> str:
        return f"{self.series} - {self.model} made by {self.maker}"


class Driver(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="driver_profile"
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    joined_date = models.DateField(auto_now_add=True)
    trips_posted = models.PositiveIntegerField(default=0)
    vehicle = models.OneToOneField(Vehicle,null=True, on_delete=models.CASCADE)


class Passenger(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="passenger_profile"
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    trips_taken = models.IntegerField()

    def __str__(self):
        return self.name


class Trip(models.Model):
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    date = models.DateTimeField()
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='driven_trips')
    status = models.CharField(max_length=20, default='scheduled')
    meeting_point = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available_seats = models.IntegerField()


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


class TripRequest(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="requests")
    passenger = models.ForeignKey(
        Passenger, on_delete=models.CASCADE, related_name="requests"
    )
    message = models.TextField()
    status = models.CharField(max_length=20, default="pending")
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.passenger.name} for {self.trip}"


class PassengerTripApproval(models.Model):
    trip_request = models.ForeignKey(TripRequest, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ("trip_request", "passenger")


class Notification(models.Model):
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.recipient.username}: {self.message[:50]}"


class DriverApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
