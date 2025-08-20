from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from products.models import Product, Favorite
from .serializers import ProductSerializer, FavoriteSerializer
from products.api.v1.permissions import IsAdminUser, IsOwnerOrAuthenticated


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', '^title','description']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    

class FavoriteViewSet(viewsets.ViewSet):
    permission_classes = [IsOwnerOrAuthenticated]

    def list(self, request):
        queryset = Favorite.objects.filter(user=request.user).select_related('product')
        serializer = FavoriteSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'detail': 'product_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            favorite = Favorite.objects.get(user=request.user, product_id=pk)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({"detail": "Favorite not found."}, status=status.HTTP_404_NOT_FOUND)