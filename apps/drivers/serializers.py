from typing import Any, Dict

from rest_framework import serializers

from apps.users.serializers import UserSerializer

from .models import Driver


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = Driver
        fields = [
            "id",
            "user",
            "latitude",
            "longitude",
            "is_online",
            "is_busy",
            "is_available",
            "vehicle_number",
            "vehicle_model",
            "last_online_at",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "last_online_at"]


class DriverLocationSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        min_value=-90,
        max_value=90,
    )
    longitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        min_value=-180,
        max_value=180,
    )

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if not attrs.get("latitude") or not attrs.get("longitude"):
            raise serializers.ValidationError(
                "Both latitude and longitude are required"
            )
        return attrs


class AvailableDriverSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)

    class Meta:
        model = Driver
        fields = [
            "id",
            "username",
            "phone_number",
            "latitude",
            "longitude",
            "vehicle_number",
            "vehicle_model",
        ]
