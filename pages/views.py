from django.shortcuts import render, get_object_or_404, redirect
from .models import Trip
from .forms import PassengerForm, ReportForm
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "pages/index.html")

def about(request):
    return render(request, "pages/about.html")


def trip(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    passenger_form = PassengerForm()
    report_form = ReportForm()
    context = {
        "trip": trip,
        "passenger_form": passenger_form,
        "report_form": report_form,
    }
    return render(request, "pages/trip.html", context)


from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from .forms import PassengerForm, ReportForm, TripForm


@login_required
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    context = {
        "trip": trip,
    }
    return render(request, "pages/trip-details.html", context)


def add_passenger(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        form = PassengerForm(request.POST)
        if form.is_valid():
            passenger = form.save(commit=False)
            passenger.trip = trip
            passenger.save()
            messages.success(request, "Passenger added successfully!")
            return redirect(reverse('trip_details', args=[trip_id]))
    return redirect(reverse('trip_details', args=[trip_id]))

def report_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.trip = trip
            report.save()
            messages.success(request, "Trip reported successfully!")
            return redirect(reverse('trip_details', args=[trip_id]))
    return redirect(reverse('trip_details', args=[trip_id]))

def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, "Trip updated successfully!")
            return redirect(reverse('trip_details', args=[trip_id]))
    else:
        form = TripForm(instance=trip)
    
    context = {
        'form': form,
        'trip': trip
    }
    return render(request, 'pages/edit_trip.html', context)

def cancel_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        trip.status = 'canceled' # type: ignore
        trip.save()
        messages.success(request, "Trip canceled successfully!")
        return redirect(reverse('trip_details', args=[trip_id]))
    return render(request, 'pages/confirm_cancel.html', {'trip': trip})

def finish_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        trip.status = 'finished' # type: ignore
        trip.save()
        messages.success(request, "Trip marked as finished!")
        return redirect(reverse('trip_details', args=[trip_id]))
    return render(request, 'pages/confirm_finish.html', {'trip': trip})


def trip_list(request):
    trips = Trip.objects.all()
    context = {
        "trips": trips,
    }
    return render(request, "pages/trip-list.html", context)


from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("index")


@login_required
def dashboard(request):
    user = request.user
    trips = Trip.objects.all()
    upcoming_trips = Trip.objects.filter(status="scheduled").order_by("date")[:5]

    if user.is_superuser:
        trips = Trip.objects.all()
    elif hasattr(user, "driver"):
        trips = Trip.objects.filter(driver=user.driver)
    elif hasattr(user, "passenger"):
        trips = Trip.objects.filter(passengers__in=[user.passenger])

    context = {
        "trips": trips,
        "upcoming_trips": upcoming_trips,
    }

    return render(request, "accounts/dashboard.html", context)
