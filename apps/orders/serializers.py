from typing import Any, Dict

from rest_framework import serializers

from apps.drivers.serializers import AvailableDriverSerializer
from apps.users.serializers import UserSerializer

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    driver_detail = AvailableDriverSerializer(source="driver", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "client",
            "driver",
            "driver_detail",
            "status",
            "pickup_latitude",
            "pickup_longitude",
            "pickup_address",
            "dropoff_latitude",
            "dropoff_longitude",
            "dropoff_address",
            "notes",
            "created_at",
            "updated_at",
            "assigned_at",
            "completed_at",
        ]
        read_only_fields = [
            "id",
            "driver",
            "status",
            "created_at",
            "updated_at",
            "assigned_at",
            "completed_at",
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "pickup_latitude",
            "pickup_longitude",
            "pickup_address",
            "dropoff_latitude",
            "dropoff_longitude",
            "dropoff_address",
            "notes",
        ]

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if not attrs.get("pickup_latitude") or not attrs.get("pickup_longitude"):
            raise serializers.ValidationError(
                "Pickup latitude and longitude are required"
            )
        return attrs


class OrderListSerializer(serializers.ModelSerializer):
    client_username = serializers.CharField(source="client.username", read_only=True)
    driver_username = serializers.CharField(
        source="driver.user.username", read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "client_username",
            "driver_username",
            "status",
            "pickup_address",
            "dropoff_address",
            "created_at",
            "assigned_at",
            "completed_at",
        ]
