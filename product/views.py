from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response

from product.models import Product
from product.serializers import ProductSerializer, ProductUpdateSerializer, \
    ProductCreateSerializer


class ProductListAPIView(ListAPIView):
    model = Product
    queryset = Product.objects.active_products()
    serializer_class = ProductSerializer


class ProductRetUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    this view update ,retrieve and delete the product
    """
    model = Product
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    queryset = Product.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = ProductUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(self.get_serializer(instance).data, status=200)


class ProductCreateAPIView(CreateAPIView):
    model = Product
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)
