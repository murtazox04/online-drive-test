from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.drivers.models import Driver
from apps.users.models import User


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CREATED = "CREATED", "Created"
        ASSIGNED = "ASSIGNED", "Assigned"
        COMPLETED = "COMPLETED", "Completed"

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        limit_choices_to={"user_type": User.UserType.CLIENT},
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        related_name="assigned_orders",
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED,
    )

    pickup_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    pickup_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    pickup_address = models.TextField(
        blank=True,
        default="",
        help_text="Pickup location address",
    )

    dropoff_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        null=True,
        blank=True,
    )
    dropoff_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        null=True,
        blank=True,
    )
    dropoff_address = models.TextField(
        blank=True,
        default="",
        help_text="Dropoff location address",
    )

    notes = models.TextField(
        blank=True,
        default="",
        help_text="Additional notes for the order",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "created_at"]),
            models.Index(fields=["client", "status"]),
            models.Index(fields=["driver", "status"]),
        ]

    def __str__(self) -> str:
        return f"Order #{self.pk} - {self.get_status_display()}"
