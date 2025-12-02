from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User

from .permissions import IsDriver
from .serializers import (
    AvailableDriverSerializer,
    DriverLocationSerializer,
    DriverSerializer,
)
from .services import DriverService


class DriverOnlineView(APIView):
    permission_classes = [IsDriver]
    serializer_class = DriverSerializer

    @extend_schema(
        tags=["Drivers"],
        summary="Set driver online",
        description=(
            "Marks the authenticated driver as online and available for order "
            "assignments. The driver must have their location set before "
            "receiving orders."
        ),
        responses={
            200: DriverSerializer,
            401: {"description": "Authentication credentials were not provided"},
            403: {"description": "Only drivers can perform this action"},
        },
    )
    def post(self, request):
        user: User = request.user
        driver = DriverService.get_or_create_driver(user)
        driver = DriverService.set_driver_online(driver)

        serializer = DriverSerializer(driver)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DriverOfflineView(APIView):
    permission_classes = [IsDriver]
    serializer_class = DriverSerializer

    @extend_schema(
        tags=["Drivers"],
        summary="Set driver offline",
        description=(
            "Marks the authenticated driver as offline and unavailable for "
            "order assignments. The driver will stop receiving new orders."
        ),
        responses={
            200: DriverSerializer,
            401: {"description": "Authentication credentials were not provided"},
            403: {"description": "Only drivers can perform this action"},
        },
    )
    def post(self, request):
        user: User = request.user
        driver = DriverService.get_or_create_driver(user)
        driver = DriverService.set_driver_offline(driver)

        serializer = DriverSerializer(driver)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DriverLocationUpdateView(APIView):
    permission_classes = [IsDriver]

    @extend_schema(
        tags=["Drivers"],
        summary="Update driver location",
        description=(
            "Updates the authenticated driver's current GPS coordinates. "
            "The driver must have a valid location set to be eligible for "
            "automatic order assignments."
        ),
        request=DriverLocationSerializer,
        responses={
            200: DriverSerializer,
            400: {"description": "Invalid location data provided"},
            401: {"description": "Authentication credentials were not provided"},
            403: {"description": "Only drivers can perform this action"},
        },
    )
    def patch(self, request):
        user: User = request.user
        serializer = DriverLocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        driver = DriverService.get_or_create_driver(user)
        driver = DriverService.update_driver_location(
            driver,
            serializer.validated_data["latitude"],  # type: ignore
            serializer.validated_data["longitude"],  # type: ignore
        )

        response_serializer = DriverSerializer(driver)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class DriverStatusView(APIView):
    permission_classes = [IsDriver]

    @extend_schema(
        tags=["Drivers"],
        summary="Get driver status",
        description=(
            "Returns the current status of the authenticated driver including "
            "online status, busy status, availability, and location."
        ),
        responses={
            200: {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "is_online": {"type": "boolean"},
                    "is_busy": {"type": "boolean"},
                    "is_available": {"type": "boolean"},
                    "latitude": {"type": "number", "nullable": True},
                    "longitude": {"type": "number", "nullable": True},
                    "vehicle_number": {"type": "string"},
                    "vehicle_model": {"type": "string"},
                    "last_online_at": {"type": "string", "format": "date-time"},
                },
            },
            401: {"description": "Authentication credentials were not provided"},
            403: {"description": "Only drivers can perform this action"},
        },
    )
    def get(self, request):
        user: User = request.user
        driver = DriverService.get_or_create_driver(user)
        driver_status = DriverService.get_driver_status(driver)

        return Response(driver_status, status=status.HTTP_200_OK)


class AvailableDriversListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Drivers"],
        summary="Get all available drivers",
        description=(
            "Returns a list of all drivers who are currently online, not busy, "
            "and have their location set. These drivers are available for "
            "automatic order assignments."
        ),
        responses={
            200: AvailableDriverSerializer(many=True),
            401: {"description": "Authentication credentials were not provided"},
        },
    )
    def get(self, request):
        available_drivers = DriverService.get_available_drivers()
        serializer = AvailableDriverSerializer(available_drivers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
