from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from ..models import Order
from .serializers import OrderSerializer, OrderUpdateSerializer, OrderCreateSerializer
from .permissions import IsCustomerUser, IsBusinessUserForOrder
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderListCreateView(generics.ListCreateAPIView):
    """List related orders and allow customers to create new orders."""

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return orders where the authenticated user is customer or business user."""
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        )

    def get_serializer_class(self):
        """Use the creation serializer for POST and the read serializer otherwise."""
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        """Apply customer-specific permissions for order creation requests."""
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """Create an order from an offer detail and return the full order payload."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )


class OrderUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete single orders with method-specific permissions."""

    queryset = Order.objects.all()

    def get_serializer_class(self):
        """Use the update serializer for PATCH and the read serializer otherwise."""
        if self.request.method == 'PATCH':
            return OrderUpdateSerializer
        return OrderSerializer

    def get_permissions(self):
        """Restrict deletion to admins and updates to the assigned business user."""
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsBusinessUserForOrder()]
        return [IsAuthenticated()]


class OrderCountView(APIView):
    """Return the number of in-progress orders for a business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """Count in-progress orders after confirming the target user exists."""
        if not User.objects.filter(id=business_user_id).exists():
            return Response(
                {'detail': 'Business user not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        count = Order.objects.filter(
            business_user_id=business_user_id,
            status='in_progress'
        ).count()
        return Response({'order_count': count})


class CompletedOrderCountView(APIView):
    """Return the number of completed orders for a business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """Count completed orders after confirming the target user exists."""
        if not User.objects.filter(id=business_user_id).exists():
            return Response(
                {'detail': 'Business user not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        count = Order.objects.filter(
            business_user_id=business_user_id,
            status='completed'
        ).count()
        return Response({'completed_order_count': count})
