from rest_framework import serializers

from orders.models import Order, OrderProduct, OrderState
from product.serializers import ProductSerializer
from user.serializers import UserSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderProduct
        fields = [
            'ordered',
            'product',
            'quantity',
        ]


# class OrderSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     order_products = OrderProductSerializer(many=True, read_only=True, required=False)
#     order_state = serializers.ChoiceField(required=False, allow_blank=True, choices=OrderState)
#
#     class Meta:
#         model = Order
#
#         fields = [
#             'user',
#             'order_products',
#             'start_date',
#             'ref_code',
#             'ordered',
#             'order_products',
#             'order_state',
#             'ordered_date',
#         ]


class OrderSerializer(serializers.ModelSerializer):
    order_products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'order_products',
        )

    def get_order_products(self):



CartActions = (
    ('ADD', 'ADD'),
    ('REMOVE', 'REMOVE'),
)


class CartActionSerializer(serializers.Serializer):
    product_slug = serializers.SlugField()
    action = serializers.ChoiceField(choices=CartActions)


class OrderStateSerializer(serializers.Serializer):
    order_state = serializers.ChoiceField(choices=OrderState)
