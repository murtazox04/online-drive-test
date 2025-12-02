from decimal import Decimal
from typing import Any, Dict, Final

from django.core.cache import cache
from django.db.models import QuerySet
from django.utils import timezone

from apps.users.models import User

from .models import Driver


class DriverService:
    CACHE_KEY_PREFIX: Final[str] = "available_drivers"
    CACHE_TIMEOUT: Final[int] = 60

    @staticmethod
    def get_or_create_driver(user: User) -> Driver:
        driver, created = Driver.objects.get_or_create(user=user)
        return driver

    @staticmethod
    def set_driver_online(driver: Driver) -> Driver:
        driver.is_online = True
        driver.last_online_at = timezone.now()
        driver.save(update_fields=["is_online", "last_online_at"])
        cache.delete(DriverService.CACHE_KEY_PREFIX)
        return driver

    @staticmethod
    def set_driver_offline(driver: Driver) -> Driver:
        driver.is_online = False
        driver.save(update_fields=["is_online"])
        cache.delete(DriverService.CACHE_KEY_PREFIX)
        return driver

    @staticmethod
    def update_driver_location(
        driver: Driver, latitude: Decimal, longitude: Decimal
    ) -> Driver:
        driver.latitude = latitude
        driver.longitude = longitude
        driver.save(update_fields=["latitude", "longitude"])
        cache.delete(DriverService.CACHE_KEY_PREFIX)
        return driver

    @staticmethod
    def set_driver_busy(driver: Driver, is_busy: bool) -> Driver:
        driver.is_busy = is_busy
        driver.save(update_fields=["is_busy"])
        if is_busy:
            cache.delete(DriverService.CACHE_KEY_PREFIX)
        return driver

    @staticmethod
    def get_available_drivers() -> QuerySet[Driver]:
        if cached_ids := cache.get(DriverService.CACHE_KEY_PREFIX):
            return Driver.objects.filter(id__in=cached_ids).select_related("user")

        available_drivers = (
            Driver.objects.filter(is_online=True, is_busy=False)
            .exclude(latitude__isnull=True, longitude__isnull=True)
            .select_related("user")
        )

        if driver_ids := list(available_drivers.values_list("id", flat=True)):
            cache.set(
                DriverService.CACHE_KEY_PREFIX, driver_ids, DriverService.CACHE_TIMEOUT
            )

        return available_drivers

    @staticmethod
    def get_driver_status(driver: Driver) -> Dict[str, Any]:
        return {
            "is_online": driver.is_online,
            "is_busy": driver.is_busy,
            "is_available": driver.is_available,
            "latitude": driver.latitude,
            "longitude": driver.longitude,
            "last_online_at": driver.last_online_at,
        }
