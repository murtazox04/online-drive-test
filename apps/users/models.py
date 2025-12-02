from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class UserType(models.TextChoices):
        DRIVER = "DRIVER", "Driver"
        CLIENT = "CLIENT", "Client"

    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        help_text="Type of user: driver or client",
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        default="",
        help_text="User's phone number",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.username} ({self.get_user_type_display()})"
