from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("trip/<int:trip_id>/", views.trip, name="trip"),
    path("trip-details/<int:trip_id>/", views.trip_detail, name="trip_details"),
    path("trip/add/", views.add_trip, name="add_trip"),
    path("trip/<int:trip_id>/edit/", views.edit_trip, name="edit_trip"),  # type: ignore
    path("trip/search/", views.trip_search, name="trip_search"),
    path(
        "trip/<int:trip_id>/request/", views.send_trip_request, name="send_trip_request"
    ),
    path("trip/<int:trip_id>/cancel/", views.cancel_trip, name="cancel_trip"),
    path("trip/<int:trip_id>/finish/", views.finish_trip, name="finish_trip"),
    path(
        "trip/<int:trip_id>/add-passenger/", views.add_passenger, name="add_passenger"
    ),
    path("trip/<int:trip_id>/report/", views.report_trip, name="report_trip"),
    path("trips/", views.trip_list, name="trip_list"),  # Add this line
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),  # type: ignore
    path("dashboard/", views.dashboard, name="dashboard"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("trip/<int:trip_id>/delete/", views.delete_trip, name="delete_trip"),
    path(
        "trip_request/<int:trip_request_id>/details/",
        views.trip_request_details,
        name="trip_request_details",
    ),
    # New URL patterns for trip request actions
    path(
        "trip_request/<int:trip_request_id>/pre_accept/",
        views.pre_accept_trip_request,
        name="pre_accept_trip_request",
    ),
    path(
        "trip_request/<int:trip_request_id>/accept/",
        views.accept_trip_request,
        name="accept_trip_request",
    ),
    path(
        "trip_request/<int:trip_request_id>/passenger_approve/",
        views.passenger_approve_request,
        name="passenger_approve_request",
    ),
    # Admin-specific URL patterns
    path(
        "administration/user/<int:user_id>/actions/",
        views.admin_user_actions,
        name="admin_user_actions",
    ),
    path(
        "administration/trip/<int:trip_id>/actions/",
        views.admin_trip_actions,
        name="admin_trip_actions",
    ),
    path(
        "administration/send_notification/",
        views.send_notification,
        name="send_notification",
    ),
    path(
        "administration/driver/<int:driver_id>/stats/",
        views.driver_stats,
        name="driver_stats",
    ),
    path("apply_as_driver/", views.apply_as_driver, name="apply_as_driver"),
]
