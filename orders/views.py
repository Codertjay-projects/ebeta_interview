import random
import string

from django.db.models import Q
from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import OrderProduct, Order
from orders.serializers import CartActionSerializer, OrderStateSerializer, OrderSerializer
from product.models import Product


class UserOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order = Order.objects.filter(user=request.user, ordered=False).first()
        print(order)
        if not order:
            order = Order.objects.create(user=request.user, ordered=False)
        print('the order',order)
        return Response({'message': 'User Current Order', 'data': OrderSerializer(instance=order).data}, status=200)


class UserOrderHistory(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            Q(order_state='CANCELED') |
            Q(order_state='DELIVERED') &
            Q(ordered=True) &
            Q(user=self.request.user)
        ).distinct()


class AddOrRemoveProductFromCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CartActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        product_slug = data.get('product_slug')
        action = data.get('action')
        product = Product.objects.filter(slug=product_slug).first()
        if not product:
            return Response({'message': 'Product does not exist'}, status=400)
        order_product = OrderProduct.objects.filter(user=request.user, product=product, ordered=False).first()
        if not order_product:
            order_product = OrderProduct.objects.create(user=request.user, ordered=False, product=product)
        order, created = Order.objects.get_or_create(user=request.user, ordered=False)

        if order.order_products.filter(product__slug=product.slug).exists():
            if action == 'add':
                order_product.quantity += 1
            elif action == 'remove':
                if order_product.quantity <= 1:
                    order.order_products.remove(order_product)
                    order_product.delete()
                else:
                    order_product.quantity -= 1
            order_product.save()
            order.save()
            print('order')
            return Response({'message': 'Product quantity updated', 'data': OrderSerializer(instance=order).data})
        else:
            if action == 'add':
                order.order_products.add(order_product)
                order_product.quantity = 1
                order_product.save()
            return Response(
                {'message': 'Product was added to cart', 'data': OrderSerializer(instance=order).data}, )


class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self):
        order = Order.objects.filter(user=self.request.user, ordered=False).first()
        if not order:
            return Response({'message': 'Please create and order by adding product to your cart'}, status=404)
        if order.get_total <= 0:
            return Response({'Message': 'You currently dont have product in your cart'}, status=400)
        order_products = order.order_products.all()
        order_products.update(ordered=True)
        for product in order_products:
            product.save()
        order.ordered = True
        order.ordered_date = timezone.now()
        order.ref_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
        order.save()
        return Response({'message': 'Successfully checkout', 'data': OrderSerializer(instance=order).data}, status=200)


class UpdateOrderState(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        order_ref = kwargs.get('order_ref')
        serializer = OrderStateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = Order.objects.filter(order_ref=order_ref, ordered=True, user=request.user).first()
        if not order:
            return Response({'message': 'An active order with this ref code doesnt exist '}, status=404)
        order.order_state = serializer.data.get('order_state')
        return Response({'message': 'Order was successfully updated',
                         'data': OrderSerializer(instance=order).data}, status=200)
