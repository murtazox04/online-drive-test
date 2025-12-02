from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from .models import Driver
from .services import DriverService

User = get_user_model()


@pytest.mark.django_db
class TestDriverModel:
    def test_driver_creation(self, driver_user):
        driver = Driver.objects.create(
            user=driver_user,
            latitude=Decimal("40.712776"),
            longitude=Decimal("-74.005974"),
        )
        assert driver.user == driver_user
        assert driver.is_online is False
        assert driver.is_busy is False

    def test_driver_is_available(self, driver_profile):
        assert driver_profile.is_available is True
        driver_profile.is_busy = True
        driver_profile.save()
        assert driver_profile.is_available is False


@pytest.mark.django_db
class TestDriverService:
    def test_get_or_create_driver(self, driver_user):
        driver = DriverService.get_or_create_driver(driver_user)
        assert isinstance(driver, Driver)
        assert driver.user == driver_user

        driver2 = DriverService.get_or_create_driver(driver_user)
        assert driver == driver2

    def test_set_driver_online(self, driver_profile):
        driver_profile.is_online = False
        driver_profile.save()

        driver = DriverService.set_driver_online(driver_profile)
        assert driver.is_online is True
        assert driver.last_online_at is not None

    def test_set_driver_offline(self, driver_profile):
        driver = DriverService.set_driver_offline(driver_profile)
        assert driver.is_online is False

    def test_update_driver_location(self, driver_profile):
        new_lat = Decimal("40.758896")
        new_lng = Decimal("-73.985130")

        driver = DriverService.update_driver_location(driver_profile, new_lat, new_lng)
        assert driver.latitude == new_lat
        assert driver.longitude == new_lng

    def test_get_available_drivers(self, driver_profile):
        available_drivers = DriverService.get_available_drivers()
        assert driver_profile in available_drivers

        DriverService.set_driver_busy(driver_profile, is_busy=True)
        available_drivers = DriverService.get_available_drivers()
        assert driver_profile not in available_drivers
