from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.OrderCreateView.as_view(), name="order-create"),
    path("my-orders/", views.UserOrdersListView.as_view(), name="user-orders"),
    path("<int:order_id>/", views.OrderDetailView.as_view(), name="order-detail"),
    path(
        "<int:order_id>/complete/",
        views.OrderCompleteView.as_view(),
        name="order-complete",
    ),
]
