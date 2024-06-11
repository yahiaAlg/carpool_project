from django.contrib import admin
from .models import (
    Vehicle,
    Driver,
    Passenger,
    Trip,
    Report,
    TripRequest,
    PassengerTripApproval,
    Notification,
    DriverApplication,
)

# Register your models here.


class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "license_plate",
        "air_conditioned",
        "maker",
        "model",
        "series",
        "type",
        "max_seats",
    )
    search_fields = (
        "license_plate",
        "maker",
        "model",
        "series",
        "type",
    )
    list_filter = (
        "air_conditioned",
        "maker",
        "model",
        "series",
        "type",
        "max_seats",
    )


class DriverAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "phone",
        "age",
        "gender",
        "joined_date",
        "trips_posted",
        "vehicle",
    )
    search_fields = ("name", "phone", "user__username")
    list_filter = ("gender", "joined_date", "trips_posted")


class PassengerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "phone",
        "gender",
        "age",
        "trips_taken",
    )
    search_fields = ("name", "phone", "user__username")
    list_filter = ("gender", "trips_taken")


class TripAdmin(admin.ModelAdmin):
    list_display = (
        "from_location",
        "to_location",
        "date",
        "driver",
        "status",
        "meeting_point",
        "price",
        "available_seats",
    )
    search_fields = (
        "from_location",
        "to_location",
        "driver__username",  # Assuming you want to search by driver's username
        "status",
        "meeting_point",
    )
    list_filter = (
        "date",
        "status",
        "driver",
    )


class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "trip",
        "content",
        "reported_by",
        "date_reported",
    )
    search_fields = ("trip__id", "reported_by", "content")  # Search by trip ID
    list_filter = ("date_reported",)


class TripRequestAdmin(admin.ModelAdmin):
    list_display = (
        "trip",
        "passenger",
        "message",
        "status",
        "requested_at",
    )
    search_fields = (
        "trip__from_location",
        "trip__to_location",
        "passenger__name",
        "status",
    )
    list_filter = ("status", "requested_at")


class PassengerTripApprovalAdmin(admin.ModelAdmin):
    list_display = (
        "trip_request",
        "passenger",
        "approved",
    )
    search_fields = (
        "trip_request__trip__from_location",
        "trip_request__trip__to_location",
        "passenger__name",
    )
    list_filter = ("approved",)


class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "recipient",
        "message",
        "is_read",
        "created_at",
    )
    search_fields = (
        "recipient__username",
        "message",
    )
    list_filter = ("is_read", "created_at")


class DriverApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("user__username", "status")
    list_filter = ("status", "created_at", "updated_at")


# Register the models with their custom admin classes
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(TripRequest, TripRequestAdmin)
admin.site.register(PassengerTripApproval, PassengerTripApprovalAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(DriverApplication, DriverApplicationAdmin)
