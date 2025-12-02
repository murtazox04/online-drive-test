from django.urls import path

from . import views

app_name = "drivers"

urlpatterns = [
    path("online/", views.DriverOnlineView.as_view(), name="driver-online"),
    path("offline/", views.DriverOfflineView.as_view(), name="driver-offline"),
    path("location/", views.DriverLocationUpdateView.as_view(), name="driver-location"),
    path("status/", views.DriverStatusView.as_view(), name="driver-status"),
    path(
        "available/", views.AvailableDriversListView.as_view(), name="available-drivers"
    ),
]
