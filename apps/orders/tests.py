from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from .models import Order
from .services import OrderService

User = get_user_model()


@pytest.mark.django_db
class TestOrderModel:
    def test_order_creation(self, client_user):
        order = Order.objects.create(
            client=client_user,
            pickup_latitude=Decimal("40.712776"),
            pickup_longitude=Decimal("-74.005974"),
            pickup_address="123 Main St",
        )
        assert order.client == client_user
        assert order.status == Order.OrderStatus.CREATED
        assert order.driver is None

    def test_order_str(self, order):
        assert f"Order #{order.pk}" in str(order)


@pytest.mark.django_db
class TestOrderService:
    def test_create_order(self, client_user):
        order = OrderService.create_order(
            client=client_user,
            pickup_latitude=Decimal("40.712776"),
            pickup_longitude=Decimal("-74.005974"),
            pickup_address="123 Main St",
        )
        assert order.client == client_user
        assert order.status in [Order.OrderStatus.CREATED, Order.OrderStatus.ASSIGNED]

    def test_create_order_non_client(self, driver_user):
        with pytest.raises(ValidationError):
            OrderService.create_order(
                client=driver_user,
                pickup_latitude=Decimal("40.712776"),
                pickup_longitude=Decimal("-74.005974"),
            )

    def test_assign_order_to_driver(self, order, driver_profile):
        order.status = Order.OrderStatus.CREATED
        order.driver = None
        order.save()

        assigned_order = OrderService.assign_order_to_driver(order, driver_profile)
        assert assigned_order.driver == driver_profile
        assert assigned_order.status == Order.OrderStatus.ASSIGNED
        assert assigned_order.assigned_at is not None

    def test_complete_order(self, order, driver_profile):
        order.status = Order.OrderStatus.ASSIGNED
        order.driver = driver_profile
        order.save()

        completed_order = OrderService.complete_order(order)
        assert completed_order.status == Order.OrderStatus.COMPLETED
        assert completed_order.completed_at is not None

    def test_get_user_orders_client(self, client_user, order):
        orders = OrderService.get_user_orders(client_user)
        assert order in orders

    def test_get_user_orders_driver(self, driver_user, driver_profile, order):
        order.driver = driver_profile
        order.save()

        orders = OrderService.get_user_orders(driver_user)
        assert order in orders
