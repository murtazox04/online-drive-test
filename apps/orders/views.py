from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.drivers.permissions import IsDriver
from apps.users.models import User

from .permissions import IsClient
from .serializers import (
    OrderCreateSerializer,
    OrderListSerializer,
    OrderSerializer,
)
from .services import OrderService


class OrderCreateView(APIView):
    permission_classes = [IsClient]

    @extend_schema(
        tags=["Orders"],
        summary="Create new order",
        description=(
            "Creates a new order for the authenticated client. The order will be "
            "automatically assigned to an available driver if one exists. "
            "Otherwise, it remains in CREATED status until a driver becomes "
            "available."
        ),
        request=OrderCreateSerializer,
        responses={
            201: OrderSerializer,
            400: {"description": "Invalid order data provided"},
            401: {"description": "Authentication credentials were not provided"},
            403: {"description": "Only clients can create orders"},
        },
    )
    def post(self, request):
        user: User = request.user
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = OrderService.create_order(client=user, **serializer.validated_data)  # type: ignore

        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class UserOrdersListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Orders"],
        summary="Get my orders",
        description=(
            "Returns all orders for the authenticated user. "
            "For clients: returns all orders they have created. "
            "For drivers: returns all orders assigned to them."
        ),
        responses={
            200: OrderListSerializer(many=True),
            401: {"description": "Authentication credentials were not provided"},
        },
    )
    def get(self, request):
        user: User = request.user
        orders = OrderService.get_user_orders(user)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Orders"],
        summary="Get order details",
        description=(
            "Returns detailed information about a specific order. "
            "Users can only view orders they are associated with "
            "(as client or assigned driver)."
        ),
        parameters=[
            OpenApiParameter(
                name="order_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID of the order to retrieve",
            ),
        ],
        responses={
            200: OrderSerializer,
            401: {"description": "Authentication credentials were not provided"},
            403: {"description": "You don't have permission to view this order"},
            404: {"description": "Order not found"},
        },
    )
    def get(self, request, order_id):
        order = OrderService.get_order_details(order_id)
        if not order:
            raise NotFound("Order not found")

        user: User = request.user
        if order.client != user and (
            not hasattr(user, "driver_profile") or order.driver != user.driver_profile
        ):
            raise PermissionDenied("You don't have permission to view this order")

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCompleteView(APIView):
    permission_classes = [IsDriver]
    serializer_class = OrderSerializer

    @extend_schema(
        tags=["Orders"],
        summary="Complete order",
        description=(
            "Marks an order as completed. Only the driver assigned to the order "
            "can complete it. This action sets the order status to COMPLETED "
            "and marks the driver as available for new assignments."
        ),
        parameters=[
            OpenApiParameter(
                name="order_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID of the order to complete",
            ),
        ],
        responses={
            200: OrderSerializer,
            401: {"description": "Authentication credentials were not provided"},
            403: {
                "description": (
                    "Only drivers can perform this action or "
                    "you can only complete your own orders"
                )
            },
            404: {"description": "Order not found"},
        },
    )
    def patch(self, request, order_id):
        user: User = request.user
        order = OrderService.get_order_details(order_id)
        if not order:
            raise NotFound("Order not found")

        if not hasattr(user, "driver_profile") or order.driver != user.driver_profile:
            raise PermissionDenied("You can only complete your own orders")

        order = OrderService.complete_order(order)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
