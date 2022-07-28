from rest_framework import serializers

from order.models import Order, OrderProduct, OrderState
from product.serializers import ProductSerializer
from user.serializers import UserSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderProduct
        fields = [
            'user',
            'ordered',
            'product',
            'quantity',
        ]


class OrderTestSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    products = OrderProductSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = [
            'user',
            'ordered',
            'products',
        ]


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    products = OrderProductSerializer(many=True, read_only=True, required=False)
    order_state = serializers.ChoiceField(required=False, allow_blank=True, choices=OrderState)

    class Meta:
        model = Order
        fields = [
            'user',
            'products',
            'start_date',
            'ref_code',
            'ordered',
            'products',
            'order_state',
            'ordered_date',
        ]


CartActions = (
    ('ADD', 'ADD'),
    ('REMOVE', 'REMOVE'),
)


class CartActionSerializer(serializers.Serializer):
    product_slug = serializers.SlugField()
    action = serializers.ChoiceField(choices=CartActions)


class OrderStateSerializer(serializers.Serializer):
    order_state = serializers.ChoiceField(choices=OrderState)
