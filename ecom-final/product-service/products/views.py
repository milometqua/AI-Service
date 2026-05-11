from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .models import Category, Product, Book, Electronics, Fashion
from .serializers import (CategorySerializer, ProductSerializer,
                           ProductCreateSerializer, BookDetailSerializer,
                           ElectronicsDetailSerializer, FashionDetailSerializer)


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'rating', 'sold_count', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related(
            'category', 'book_detail', 'electronics_detail', 'fashion_detail'
        )
        product_type = self.request.query_params.get('type')
        category = self.request.query_params.get('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if product_type:
            queryset = queryset.filter(product_type=product_type)
        if category:
            queryset = queryset.filter(category__slug=category)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class ProductSearchView(APIView):
    """Full-text search sản phẩm theo tên, mô tả, tác giả (book)"""
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Vui lòng nhập từ khóa tìm kiếm.'}, status=400)

        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(book_detail__author__icontains=query),
            is_active=True
        ).distinct()[:20]

        return Response(ProductSerializer(products, many=True).data)


class ProductStockCheckView(APIView):
    """Endpoint nội bộ: kiểm tra tồn kho (dùng bởi order-service)"""
    permission_classes = [AllowAny]

    def post(self, request):
        items = request.data.get('items', [])
        result = []
        for item in items:
            try:
                product = Product.objects.get(id=item['product_id'])
                result.append({
                    'product_id': product.id,
                    'name': product.name,
                    'requested': item['quantity'],
                    'available': product.stock,
                    'sufficient': product.stock >= item['quantity'],
                    'price': str(product.price),
                })
            except Product.DoesNotExist:
                result.append({'product_id': item['product_id'], 'error': 'Không tìm thấy sản phẩm'})
        return Response(result)
