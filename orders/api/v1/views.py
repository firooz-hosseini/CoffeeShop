from rest_framework import viewsets,permissions
from .serializers import OrderSerializer,CommentSerializer
from orders.models import Order,Notification,Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        admins = User.objects.filter(is_staff=True)
        for admin in admins:
            Notification.objects.create(message=f"new order by{self.request.user.first_name}")
        return order

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)