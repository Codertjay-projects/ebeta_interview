from rest_framework import serializers

from store.models import Store


class StoreSerializer(serializers.ModelSerializer):
    """
    Store serializer used for CRUD
    """
    name = serializers.CharField(required=False, allow_blank=True, max_length=250)
    image = serializers.ImageField(required=False)
    description = serializers.CharField(required=False, allow_blank=True, max_length=1000)

    class Meta:
        model = Store
        read_only_fields = ['id','slug']
        fields = ['id','slug', 'name', 'image', 'description', ]
