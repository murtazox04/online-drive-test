from django.contrib import admin

from .models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "is_online",
        "is_busy",
        "is_available",
        "vehicle_number",
        "latitude",
        "longitude",
        "last_online_at",
    ]
    list_filter = ["is_online", "is_busy", "created_at"]
    search_fields = ["user__username", "user__email", "vehicle_number"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-last_online_at"]

    def is_available(self, obj: Driver) -> bool:
        return obj.is_available

    is_available.boolean = True
    is_available.short_description = "Available"
