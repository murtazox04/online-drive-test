from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.users.models import User


class Driver(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="driver_profile",
        limit_choices_to={"user_type": User.UserType.DRIVER},
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        null=True,
        blank=True,
        help_text="Driver's current latitude",
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        null=True,
        blank=True,
        help_text="Driver's current longitude",
    )

    is_online = models.BooleanField(
        default=False,
        help_text="Whether driver is currently online",
    )
    is_busy = models.BooleanField(
        default=False,
        help_text="Whether driver is currently busy with an order",
    )

    vehicle_number = models.CharField(
        max_length=20,
        blank=True,
        default="",
        help_text="Vehicle registration number",
    )
    vehicle_model = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Vehicle model",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_online_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "drivers"
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_online", "is_busy"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self) -> str:
        return f"{self.user.username} - {'Online' if self.is_online else 'Offline'}"

    @property
    def is_available(self) -> bool:
        return self.is_online and not self.is_busy
