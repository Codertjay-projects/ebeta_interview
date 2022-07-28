from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from product.serializers import ProductSerializer
from store.models import Store
from store.serializers import StoreSerializer


class StoreViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    lookup_field = 'slug'


class StoreProducts(APIView):

    def get(self, request, **kwargs):
        store_slug = self.kwargs.get('store_slug')
        store = Store.objects.filter(slug=store_slug).first()
        if not store:
            return Response({'message': 'Store does not exist'}, status=200)
        return Response(
            {'message': 'Store products',
             'data': ProductSerializer(store.product_set.all(), many=True).data}, status=200)
