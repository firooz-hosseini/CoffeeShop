from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from products.models import Product, Category, Favorite, Image
from rest_framework.response import Response
from .serializers import ProductSerializer, FavoriteSerializer,CategorySerializer, ImageSerializer
from rest_framework.permissions import IsAdminUser

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', '^title','description', 'quantity', 'tags']
    filterset_fields = ['category']
    ordering_fields = ['price', 'title', 'quantity']
    ordering = ['id']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser])
    def upload_image(self, request, id=None):
        product = self.get_object()
        files = request.FILES.getlist('images')
        is_main_flags = request.data.getlist('is_main')
        replace = request.data.get('replace', 'false').lower() == 'true'

        if not files:
            return Response({'error': 'No images uploaded'}, status=400)

        if replace:
            product.image_product.all().delete()
            main_found = False
        else:
            main_found = product.image_product.filter(is_main=True).exists()


        created_images = []
        for i, img_file in enumerate(files):
            is_main = is_main_flags[i].lower() == 'true' if i < len(is_main_flags) else False
            if is_main:
                if main_found:
                    is_main = False
                else:
                    main_found = True
            image_obj = Image.objects.create(product=product, image=img_file, is_main=is_main)
            created_images.append(image_obj)

        serializer = ImageSerializer(created_images, many=True)
        return Response(serializer.data, status=201)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]  
    

class FavoriteViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

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
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        serializer = FavoriteSerializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            favorite = Favorite.objects.get(user=request.user, product_id=pk)
            favorite.delete()
            return Response({'detail': 'Deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({'detail': 'Favorite not found.'}, status=status.HTTP_404_NOT_FOUND)