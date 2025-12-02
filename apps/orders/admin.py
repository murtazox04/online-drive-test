from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "client",
        "driver",
        "status",
        "pickup_address",
        "created_at",
        "assigned_at",
        "completed_at",
    ]
    list_filter = ["status", "created_at", "assigned_at", "completed_at"]
    search_fields = [
        "client__username",
        "driver__user__username",
        "pickup_address",
        "dropoff_address",
    ]
    readonly_fields = ["created_at", "updated_at", "assigned_at", "completed_at"]
    ordering = ["-created_at"]

    fieldsets = (
        ("Order Info", {"fields": ("client", "driver", "status", "notes")}),
        (
            "Pickup Location",
            {"fields": ("pickup_latitude", "pickup_longitude", "pickup_address")},
        ),
        (
            "Dropoff Location",
            {"fields": ("dropoff_latitude", "dropoff_longitude", "dropoff_address")},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at", "assigned_at", "completed_at")},
        ),
    )
