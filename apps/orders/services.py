from decimal import Decimal
from typing import Optional

from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.drivers.models import Driver
from apps.drivers.services import DriverService
from apps.users.models import User

from .models import Order


class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(
        client: User,
        pickup_latitude: Decimal,
        pickup_longitude: Decimal,
        pickup_address: str = "",
        dropoff_latitude: Optional[Decimal] = None,
        dropoff_longitude: Optional[Decimal] = None,
        dropoff_address: str = "",
        notes: str = "",
    ) -> Order:
        if client.user_type != User.UserType.CLIENT:
            raise ValidationError("Only clients can create orders")

        order = Order.objects.create(
            client=client,
            pickup_latitude=pickup_latitude,
            pickup_longitude=pickup_longitude,
            pickup_address=pickup_address,
            dropoff_latitude=dropoff_latitude,
            dropoff_longitude=dropoff_longitude,
            dropoff_address=dropoff_address,
            notes=notes,
            status=Order.OrderStatus.CREATED,
        )

        if available_driver := OrderService._find_available_driver():
            OrderService.assign_order_to_driver(order, available_driver)

        return order

    @staticmethod
    def _find_available_driver() -> Optional[Driver]:
        available_drivers = DriverService.get_available_drivers()
        return available_drivers.first() if available_drivers.exists() else None

    @staticmethod
    @transaction.atomic
    def assign_order_to_driver(order: Order, driver: Driver) -> Order:
        if order.status != Order.OrderStatus.CREATED:
            raise ValidationError("Order is not in CREATED status")

        if not driver.is_available:
            raise ValidationError("Driver is not available")

        order.driver = driver
        order.status = Order.OrderStatus.ASSIGNED
        order.assigned_at = timezone.now()
        order.save(update_fields=["driver", "status", "assigned_at"])

        DriverService.set_driver_busy(driver, is_busy=True)

        return order

    @staticmethod
    @transaction.atomic
    def complete_order(order: Order) -> Order:
        if order.status != Order.OrderStatus.ASSIGNED:
            raise ValidationError("Order is not in ASSIGNED status")

        order.status = Order.OrderStatus.COMPLETED
        order.completed_at = timezone.now()
        order.save(update_fields=["status", "completed_at"])

        if order.driver:
            DriverService.set_driver_busy(order.driver, is_busy=False)

        return order

    @staticmethod
    def get_user_orders(user: User) -> QuerySet[Order]:
        if user.user_type == User.UserType.CLIENT:
            return Order.objects.filter(client=user).select_related("driver__user")

        if user.user_type == User.UserType.DRIVER:
            if driver := Driver.objects.filter(user=user).first():
                return Order.objects.filter(driver=driver).select_related("client")

        return Order.objects.none()

    @staticmethod
    def get_order_details(order_id: int) -> Optional[Order]:
        return (
            Order.objects.filter(id=order_id)
            .select_related("client", "driver__user")
            .first()
        )
