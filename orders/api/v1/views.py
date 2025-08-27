from rest_framework import viewsets,permissions
from .serializers import OrderSerializer,CommentSerializer,RatingSerializer,NotificationSerializer,KitchenOrderSerializer
from orders.models import Order,Notification,Comment,Rating
from accounts.models import CustomUser
from .permissions import IsKitchenStaff

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        admins = CustomUser.objects.filter(is_staff=True)
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

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Notification.objects.all()
        return Notification.objects.none()
    
class KitchenOrderViewSet(viewsets.ModelViewSet):
    serializer_class = KitchenOrderSerializer
    permission_classes = [IsKitchenStaff]

    def get_queryset(self):
        return Order.objects.filter(status='paid').order_by('time')
    