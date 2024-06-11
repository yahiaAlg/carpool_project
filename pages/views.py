from pprint import pprint
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Trip, Passenger, TripRequest, PassengerTripApproval
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .forms import *
from django.db.models import Sum, Count


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


@login_required
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    context = {
        "trip": trip,
    }
    return render(request, "pages/trip-details.html", context)


def add_passenger(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == "POST":
        form = PassengerForm(request.POST)
        if form.is_valid():
            passenger = form.save(commit=False)
            if Passenger.objects.filter(user=passenger.user).exists():
                passenger = Passenger.objects.filter(user=passenger.user).first()
                trip.passengers.add(passenger)
                messages.success(request, "Passenger added successfully!")
            else:
                messages.warning(
                    request,
                    f"the passenger {passenger.user.username} is already in the list of passengers!",
                )
                return redirect("dashboard")
            return redirect(reverse("trip_details", args=[trip_id]))
    return redirect(reverse("trip_details", args=[trip_id]))


def report_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.trip = trip
            report.save()
            messages.success(request, "Trip reported successfully!")
            return redirect(reverse("trip_details", args=[trip_id]))
    return redirect(reverse("trip_details", args=[trip_id]))


def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == "POST":
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, "Trip updated successfully!")
            return redirect(reverse("trip_details", args=[trip_id]))
    else:
        form = TripForm(instance=trip)
    return render(request, "pages/edit_trip.html", {"form": form, "trip": trip})


def add_trip(request):
    form = TripForm()
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            try:
                new_trip = form.save(commit=False)  # Don't save yet
                new_trip.driver = request.user
                new_trip.save()  # Now save to get the ID
                print(
                    "new_trip with id",
                    new_trip.id if new_trip.id else "no id is yet to be set!",
                )
                pprint(new_trip)
                messages.success(request, "Trip Added successfully!")
            except Exception as e:
                messages.error(request, f"{e}")
                return redirect("add_trip")
            return redirect(reverse("trip_details", args=[new_trip.id]))

    context = {"form": form}  # No need for "trip" in the context
    return render(request, "pages/add_trip.html", context)


def cancel_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == "POST":
        trip.status = "canceled"  # type: ignore
        trip.save()
        messages.success(request, "Trip canceled successfully!")
        return redirect(reverse("trip_details", args=[trip_id]))
    return render(request, "pages/confirm_cancel.html", {"trip": trip})


def finish_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == "POST":
        trip.status = "finished"  # type: ignore
        trip.save()
        messages.success(request, "Trip marked as finished!")
        return redirect(reverse("trip_details", args=[trip_id]))
    return render(request, "pages/confirm_finish.html", {"trip": trip})


# views.py


@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == "POST":
        trip.delete()
        messages.success(request, "Trip deleted successfully!")
        return redirect("dashboard")
    return render(request, "pages/delete_trip.html", {"trip": trip})


@login_required
def edit_profile(request):
    user = request.user
    passenger_form = PassengerForm(instance=user.passenger_profile)
    driver_form = DriverForm(instance=getattr(user, "driver_profile", None))
    user_form = UserEditForm(instance=user)

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=user)
        passenger_form = PassengerForm(request.POST, instance=user.passenger_profile)
        driver_form = DriverForm(
            request.POST, instance=getattr(user, "driver_profile", None)
        )

        if user_form.is_valid() and passenger_form.is_valid():
            user_form.save()
            passenger_form.save()

            if driver_form.is_valid():
                driver_form.save()

            messages.success(request, "Your profile has been updated!")
            return redirect("dashboard")

    context = {
        "user_form": user_form,
        "passenger_form": passenger_form,
        "driver_form": driver_form,
    }
    return render(request, "accounts/edit_profile.html", context)


@login_required
def trip_request_details(request, trip_request_id):
    trip_request = get_object_or_404(TripRequest, id=trip_request_id)

    if request.method == "POST":
        form = TripRequestForm(request.POST, instance=trip_request)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = TripRequestForm(instance=trip_request)

    context = {
        "form": form,
        "trip_request": trip_request,
    }

    return render(request, "trip_request_details.html", context)


@login_required
def send_trip_request(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    if request.method == "POST":
        form = TripRequestForm(request.POST)
        if form.is_valid():
            trip_request = form.save(commit=False)
            trip_request.trip = trip
            trip_request.passenger = request.user.passenger_profile
            trip_request.save()
            messages.success(request, "Trip request sent successfully.")
            return redirect("trip_search")
    else:
        form = TripRequestForm()
    return render(request, "pages/send_request.html", {"form": form, "trip": trip})


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


# views.py


@login_required
def dashboard(request):
    user = request.user
    context = {}

    if user.is_superuser:
        # Admin dashboard logic
        trips = Trip.objects.all()
        trip_count = trips.count()
        trip_requests = TripRequest.objects.all()
        request_count = trip_requests.count()
        all_users = User.objects.all()
        context.update(
            {
                "trips": trips,
                "trip_requests": trip_requests,
                "trip_count": trip_count,
                "request_count": request_count,
            }
        )

    if hasattr(user, "driver_profile"):
        trips = Trip.objects.filter(driver=user)
        trip_count = trips.count()
        pending_requests_count = TripRequest.objects.filter(
            trip__in=trips, status="pending"
        ).count()

        # Gather all trip requests related to the driver's trips
        trip_requests = []
        for trip in trips:
            requests_for_trip = TripRequest.objects.filter(trip=trip)
            for trip_request in requests_for_trip:
                trip_requests.append(trip_request)

        context.update(
            {
                "trips": trips,
                "trip_count": trip_count,
                "pending_requests_count": pending_requests_count,
                "trip_requests": trip_requests,  # Add trip requests to the context
            }
        )

    if hasattr(user, "passenger_profile"):
        passenger = user.passenger_profile
        trip_requests = TripRequest.objects.filter(passenger=passenger)
        request_count = trip_requests.count()
        pending_requests_count = TripRequest.objects.filter(
            passenger=passenger, status="pending"
        ).count()

        # Get pending trip approvals for the passenger
        pending_approvals = PassengerTripApproval.objects.filter(
            passenger=passenger, approved=False
        ).count()

        pending_driver_application = None
        if hasattr(user, "driverapplication"):
            pending_driver_application = user.driverapplication

        context.update(
            {
                "trip_requests": trip_requests,
                "request_count": request_count,
                "pending_requests_count": pending_requests_count,
                "pending_approvals": pending_approvals,  # Add pending approvals to the context
                "pending_driver_application": pending_driver_application,
            }
        )

    return render(request, "accounts/dashboard.html", context)


@login_required
def admin_trip_actions(request, trip_id):
    if not request.user.is_superuser:
        return HttpResponse("You are not authorized to perform this action.")
    trip = get_object_or_404(Trip, pk=trip_id)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "cancel":
            trip.status = "cancelled"
            trip.save()
            messages.success(request, f"Trip #{trip_id} cancelled successfully.")
        elif action == "activate":
            trip.status = "scheduled"
            trip.save()
            messages.success(request, f"Trip #{trip_id} activated successfully.")
    return redirect("dashboard")


@login_required
def send_notification(request):
    if not request.user.is_superuser:
        return HttpResponse("You are not authorized to perform this action.")

    if request.method == "POST":
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save()
            messages.success(request, "Notification sent successfully.")
            return redirect("dashboard")
    else:
        form = NotificationForm()

    return render(request, "custom_admin/send_notification.html", {"form": form})


@login_required
def driver_stats(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    trips = Trip.objects.filter(driver=driver.user)
    total_trips = trips.count()
    total_revenue = trips.aggregate(Sum("price"))["price__sum"] or 0
    total_passengers = Passenger.objects.filter(trips__in=trips).count()
    total_notifications = Notification.objects.filter(recipient=driver.user).count()

    context = {
        "driver": driver,
        "total_trips": total_trips,
        "total_revenue": total_revenue,
        "total_passengers": total_passengers,
        "total_notifications": total_notifications,
    }
    return render(request, "custom_admin/driver_stats.html", context)


@login_required
def admin_user_actions(request, user_id):
    if not request.user.is_superuser:
        return HttpResponse("You are not authorized to perform this action.")

    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "toggle_active":
            user.is_active = not user.is_active
            user.save()
            messages.success(
                request,
                f'User {user.username} {"enabled" if user.is_active else "disabled"} successfully.',
            )
        elif action == "delete":
            user.delete()
            messages.success(request, f"User {user.username} deleted successfully.")

        elif action == "make_driver":
            # Create a driver profile for the user if they don't have one
            driver, created = Driver.objects.get_or_create(user=user)
            if created:
                driver.name = user.username
                driver.save()
                messages.success(
                    request, f"Driver profile created for {user.username}."
                )
            else:
                messages.warning(
                    request, f"{user.username} already has a driver profile."
                )
        elif action == "remove_driver":
            try:
                driver = Driver.objects.get(user=user)
                driver.delete()
                messages.success(
                    request, f"Driver profile removed for {user.username}."
                )
            except Driver.DoesNotExist:
                messages.warning(
                    request, f"{user.username} does not have a driver profile."
                )

    return redirect("dashboard")


@login_required
def pre_accept_trip_request(request, trip_request_id):
    trip_request = get_object_or_404(TripRequest, pk=trip_request_id)
    trip = trip_request.trip

    # Security check: Only the driver of the trip can pre-accept
    if trip.driver != request.user:
        return HttpResponse("You are not authorized to perform this action.")

    if trip_request.status == "pending":
        # Create pending approvals for each passenger already on the trip
        for passenger in trip.passengers.all():
            approval, created = PassengerTripApproval.objects.get_or_create(
                trip_request=trip_request,
                passenger=passenger,
            )
            if created:  # Only save if a new approval was created
                approval.save()

        # Automatically approve for the driver (assuming drivers also have passenger profiles)
        driver_passenger = trip.driver.passenger_profile  # type: ignore
        PassengerTripApproval.objects.filter(
            trip_request=trip_request, passenger=driver_passenger
        ).update(approved=True)

        trip_request.status = "pre_accepted"
        trip_request.save()
        messages.success(
            request,
            "Trip request pre-accepted! Waiting for other passengers to approve.",
        )
    else:
        messages.warning(request, "This trip request is not pending.")

    return redirect("dashboard")


@login_required
def accept_trip_request(request, trip_request_id):
    trip_request = get_object_or_404(TripRequest, pk=trip_request_id)
    trip = trip_request.trip

    # Check if the request is in the 'pre_accepted' state
    if trip_request.status == "pre_accepted":
        # Check if all passengers (including the driver) have approved
        all_approved = (
            PassengerTripApproval.objects.filter(
                trip_request=trip_request, approved=True
            ).count()
            == trip.passengers.count() + 1
        )

        if all_approved:
            trip_request.status = "accepted"
            trip_request.save()

            # Add the passenger to the trip and update available seats
            trip.passengers.add(trip_request.passenger)
            trip.available_seats -= 1
            trip.save()

            messages.success(request, "Trip request accepted!")
        else:
            messages.warning(request, "Waiting for all passengers to approve.")

    return redirect("dashboard")


@login_required
def passenger_approve_request(request, trip_request_id):
    trip_request = get_object_or_404(TripRequest, pk=trip_request_id)
    passenger = request.user.passenger_profile

    # Make sure the passenger is allowed to approve this request
    try:
        approval = PassengerTripApproval.objects.get(
            trip_request=trip_request, passenger=passenger
        )
    except PassengerTripApproval.DoesNotExist:
        messages.error(request, "You are not authorized to approve this request.")
        return redirect("dashboard")

    if request.method == "POST":
        approval.approved = True
        approval.save()

        messages.success(request, "You have approved the request.")

        # After a passenger approves, check if everyone has approved
        if trip_request.status == "pre_accepted":
            all_approved = (
                PassengerTripApproval.objects.filter(
                    trip_request=trip_request, approved=True
                ).count()
                == trip_request.trip.passengers.count() + 1
            )

            if all_approved:
                trip_request.status = "accepted"
                trip_request.save()
                trip_request.trip.passengers.add(trip_request.passenger)
                trip_request.trip.available_seats -= 1
                trip_request.trip.save()

    return redirect("dashboard")


@login_required
def apply_as_driver(request):
    if request.method == "POST":
        form = DriverApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(
                request,
                "Your application has been submitted successfully. You will be notified when it is reviewed.",
            )
            return redirect("dashboard")
    else:
        form = DriverApplicationForm()
    return render(request, "pages/driver_application.html", {"form": form})


def trip_search(request):
    if request.method == "POST":
        from_location = request.POST.get("from_location")
        to_location = request.POST.get("to_location")
        trips = Trip.objects.filter(
            from_location__icontains=from_location,
            to_location__icontains=to_location,
            status="scheduled",
            available_seats__gt=0,
        )
    else:
        trips = Trip.objects.filter(status="scheduled", available_seats__gt=0)
    context = {"trips": trips}
    return render(request, "pages/trip_search.html", context)
