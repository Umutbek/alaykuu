from farmer import models
from rest_framework import serializers
from user.serializers import FarmerSerializer, DistributerSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart items"""
    class Meta:
        model = models.CartItems
        fields = (
            'id', 'item', 'quantity'
        )
        read_only_fields = ('id',)


class GetCartItemSerializer(serializers.ModelSerializer):
    """Serializer for getting cart items"""
    class Meta:
        model = models.CartItems
        fields = (
            'id', 'item', 'quantity'
        )
        read_only_fields = ('id',)

        depth = 1


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

    # def update(self, instance, validated_data):
    #     instance.farmer = validated_data.get('farmer', instance.farmer)
    #     instance.distributer = validated_data.get('distributer', instance.distributer)
    #     instance.comment = validated_data.get('comment', instance.comment)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.totalCost = validated_data.get('totalCost', instance.totalCost)
    #     # self.create(validated_data.get('items'))
    #     # instance.items = validated_data.get('items', instance.items)
    #     instance.save()
    #
    #     return instance


class GetOrderSerializer(serializers.ModelSerializer):
    """Serializer for getting order"""
    items = GetCartItemSerializer(many=True, required=False, allow_null=True)
    farmer = FarmerSerializer()
    distributer = DistributerSerializer()

    class Meta:
        model = models.FarmerOrders
        fields = (
            'id', 'items', 'farmer', 'distributer', 'date', 'comment',
            'status', 'totalCost'
        )

        read_only_fields = ('id',)