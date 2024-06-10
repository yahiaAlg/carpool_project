from django import forms
from django import forms
from .models import Passenger, Report, Trip


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ["name", "phone", "gender", "age"]


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = "__all__"


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["from_location", "to_location", "date", "driver"]
