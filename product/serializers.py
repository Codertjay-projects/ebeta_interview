from django.utils import timezone
from rest_framework import serializers

from product.models import Product
from store.models import Store
from store.serializers import StoreSerializer


class ProductSerializer(serializers.ModelSerializer):
    """
    Used for listing the products and also the getting the detail of the product
    """
    name = serializers.CharField(max_length=250)
    price = serializers.FloatField(min_value=0.1)
    discount_price = serializers.FloatField(min_value=0.1)
    store = StoreSerializer()
    is_active = serializers.BooleanField(default=True)
    uploaded_date = serializers.DateField()
    image = serializers.ImageField(required=False)
    description = serializers.CharField(max_length=5000)

    class Meta:
        model = Product
        read_only_fields = ['id', 'slug']
        fields = [
            'id',
            'name',
            'price',
            'discount_price',
            'store',
            'slug',
            'is_active',
            'uploaded_date',
            'view_count',
            'description',
            'image',
            'timestamp',
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Used for listing the products and also the getting the detail of the product
    """
    id = serializers.IntegerField(required=False, read_only=True)
    name = serializers.CharField(max_length=250)
    price = serializers.FloatField(min_value=0.1)
    discount_price = serializers.FloatField(min_value=0.1)
    slug = serializers.SlugField(required=False, read_only=True)
    is_active = serializers.BooleanField(default=True)
    uploaded_date = serializers.DateField(default=timezone.now().date())
    image = serializers.ImageField(required=False)
    description = serializers.CharField(max_length=5000)
    store = StoreSerializer()

    class Meta:
        model = Product
        read_only_fields = ['id', 'slug']
        fields = [
            'id',
            'name',
            'price',
            'discount_price',
            'store',
            'slug',
            'is_active',
            'uploaded_date',
            'view_count',
            'description',
            'image',
            'timestamp',
        ]


class ProductUpdateSerializer(serializers.ModelSerializer):
    """
    Used for listing the products and also the getting the detail of the product
    """
    id = serializers.IntegerField(required=False, read_only=True)
    name = serializers.CharField(required=False, max_length=250)
    price = serializers.FloatField(required=False, min_value=0.1)
    discount_price = serializers.FloatField(required=False, min_value=0.1)
    slug = serializers.SlugField(required=False, read_only=True)
    is_active = serializers.BooleanField(required=False, default=True)
    uploaded_date = serializers.DateField(default=timezone.now().date())
    image = serializers.ImageField(required=False)
    description = serializers.CharField(required=False, max_length=5000)
    store = StoreSerializer(required=False)

    class Meta:
        model = Product
        read_only_fields = ['id', 'slug']
        fields = [
            'id',
            'name',
            'price',
            'discount_price',
            'store',
            'slug',
            'is_active',
            'uploaded_date',
            'view_count',
            'description',
            'image',
            'timestamp',
        ]
