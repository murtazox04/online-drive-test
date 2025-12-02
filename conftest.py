import pytest
from django.contrib.auth import get_user_model

from apps.drivers.models import Driver
from apps.orders.models import Order

User = get_user_model()


@pytest.fixture
def driver_user(db):
    return User.objects.create_user(
        username="driver1",
        email="driver@test.com",
        password="testpass123",
        user_type=User.UserType.DRIVER,
    )


@pytest.fixture
def client_user(db):
    return User.objects.create_user(
        username="client1",
        email="client@test.com",
        password="testpass123",
        user_type=User.UserType.CLIENT,
    )


@pytest.fixture
def driver_profile(driver_user):
    return Driver.objects.create(
        user=driver_user,
        latitude=40.712776,
        longitude=-74.005974,
        is_online=True,
        is_busy=False,
        vehicle_number="ABC123",
        vehicle_model="Toyota Camry",
    )


@pytest.fixture
def order(client_user, driver_profile):
    return Order.objects.create(
        client=client_user,
        driver=driver_profile,
        status=Order.OrderStatus.CREATED,
        pickup_latitude=40.712776,
        pickup_longitude=-74.005974,
        pickup_address="123 Main St",
        dropoff_latitude=40.758896,
        dropoff_longitude=-73.985130,
        dropoff_address="456 Broadway",
    )
