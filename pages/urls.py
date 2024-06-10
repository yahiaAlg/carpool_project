from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("trip/<int:trip_id>/", views.trip, name="trip"),
    path("trip-details/<int:trip_id>/", views.trip_detail, name="trip_details"),
    path("trip/<int:trip_id>/edit/", views.edit_trip, name="edit_trip"),
    path("trip/<int:trip_id>/cancel/", views.cancel_trip, name="cancel_trip"),
    path("trip/<int:trip_id>/finish/", views.finish_trip, name="finish_trip"),
    path(
        "trip/<int:trip_id>/add-passenger/", views.add_passenger, name="add_passenger"
    ),
    path("trip/<int:trip_id>/report/", views.report_trip, name="report_trip"),
    path("trips/", views.trip_list, name="trip_list"),  # Add this line
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"), # type: ignore
    path("dashboard/", views.dashboard, name="dashboard"),
]
