from rest_framework import viewsets,permissions, status
from .serializers import OrderSerializer,CommentSerializer,RatingSerializer,NotificationSerializer,KitchenOrderSerializer
from orders.models import Order,Notification,Comment,Rating
from accounts.models import CustomUser
from .permissions import IsKitchenStaff
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
 


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
    
class PaymentViewSet(viewsets.GenericViewSet):

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk, user=request.user,status='pending')
            order.status = 'paid'
            order.save()
            return Response({"detail": "Order successfully paid"}, status=status.HTTP_202_ACCEPTED)
        except Order.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=False,methods=['post'])
    def payall(self,request):
        orders = Order.objects.filter(user=request.user,status='pending')
        if orders.exists():
            orders.update(status='paid')
            return Response({"detail": "all orders successfully paid"}, status=status.HTTP_202_ACCEPTED)
        return Response({'detail':'No pending order found'},status=status.HTTP_404_NOT_FOUND)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


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
    queryset = Order.objects.filter(status='paid').order_by('time')
    serializer_class = KitchenOrderSerializer
    permission_classes = [IsKitchenStaff]

    