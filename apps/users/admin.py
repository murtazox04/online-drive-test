from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "username",
        "email",
        "user_type",
        "phone_number",
        "is_staff",
        "created_at",
    ]
    list_filter = ["user_type", "is_staff", "is_active"]
    search_fields = ["username", "email", "phone_number"]
    ordering = ["-created_at"]

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("user_type", "phone_number")}),
    )  # type: ignore
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("user_type", "phone_number")}),
    )
