from django import forms
from django.contrib.auth.models import User
from .models import *
from django.forms.widgets import DateTimeInput


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["phone", "age", "gender", "vehicle"]


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            "from_location",
            "to_location",
            "date",
            "meeting_point",
            "price",
            "available_seats",
        ]
        widgets = {
            "date": DateTimeInput(attrs={"type": "datetime-local"}),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ["name"]


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ["user", "phone", "gender", "age"]


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = "__all__"


class TripRequestForm(forms.ModelForm):
    class Meta:
        model = TripRequest
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
        }


class TripRequestAcceptanceForm(forms.ModelForm):
    class Meta:
        model = TripRequest
        fields = ["status"]
        widgets = {
            "status": forms.Select(
                choices=[("accepted", "Accepted"), ("rejected", "Rejected")]
            )
        }


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ["recipient", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 3}),
        }


class DriverApplicationForm(forms.ModelForm):
    class Meta:
        model = DriverApplication
        fields = []  # No fields needed since it's just a status change
