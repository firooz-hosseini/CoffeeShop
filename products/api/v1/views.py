from rest_framework import viewsets, permissions, status
from .permissions import IsAdminUser, IsOwnerOrAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from products.models import Product, Category, Favorite
from rest_framework.response import Response
from .serializers import ProductSerializer, FavoriteSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]


    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    

class FavoriteViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'product_id'
    permission_classes = [IsOwnerOrAuthenticated]


    def list(self, request):
        queryset = Favorite.objects.filter(user=request.user)
        serializer = FavoriteSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({'detail': 'product_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Favorite.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        create, favorite = Favorite.objects.get_or_create(user=request.user, product=product)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED if create else status.HTTP_200_OK)
    

    def delete(self, request, product_id=None):
        try:
            favorite = Favorite.objects.get(user=request.user, product_id=product_id)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({"detail": "Favorite not found."}, status=status.HTTP_404_NOT_FOUND)