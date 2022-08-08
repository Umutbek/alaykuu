from farmer import models
from rest_framework import serializers


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart items"""
    class Meta:
        model = models.CartItems
        fields = (
            'id', 'item', 'quantity'
        )
        read_only_fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for client order"""
    items = CartItemSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = models.FarmerOrders
        fields = (
            'id', 'items', 'farmer', 'distributer', 'date', 'comment',
            'status', 'totalCost'
        )

        read_only_fields = ('id',)

    def create(self, validated_data):

        items = validated_data.pop("items", None)
        order = models.FarmerOrders.objects.create(**validated_data)

        if items:
            for i in items:
                models.CartItems.objects.create(order=order, **i)
        return order