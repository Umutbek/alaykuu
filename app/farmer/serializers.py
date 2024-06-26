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
    # items = CartItemSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = models.FarmerOrders
        fields = (
            'id', 'items', 'farmer', 'distributer', 'date', 'comment', 'payment_status',
            'status', 'totalCost'
        )

        read_only_fields = ('id',)

    # def create(self, validated_data):
    #
    #     items = validated_data.pop("items", None)
    #     order = models.FarmerOrders.objects.create(**validated_data)
    #
    #     if items:
    #         for i in items:
    #             models.CartItems.objects.create( **i)
    #     return order

    # def update(self, instance, validated_data):
    #     instance.farmer = validated_data.get('farmer', instance.farmer)
    #     instance.distributer = validated_data.get('distributer', instance.distributer)
    #     instance.comment = validated_data.get('comment', instance.comment)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.totalCost = validated_data.get('totalCost', instance.totalCost)
    #     # self.items.set()
    #     # items = validated_data.pop('items', None)
    #     # new_list = []
    #     # if items:
    #     #     for i in items:
    #     #         saved = models.CartItems.objects.create(**i)
    #     #         new_list.append({"id": saved.id, "item": saved.item.id, "quantity": saved.quantity})
    #     # # self.create(validated_data.get('items'))
    #     # print(new_list)
    #     instance.items = validated_data.get('items', instance.items)
    #     self.items = validated_data.get('items')
    #     # itemss = validated_data.pop('items', None)
    #     order = models.FarmerOrders.objects.get(pk=instance.id)
    #     models.CartItems.objects.update(order=order,)
    #     # print(instance.items)
    #
    #     instance.save()
    #
    #     return instance


class OrderSerializerUpdate(serializers.ModelSerializer):
    """Serializer for client order"""
    class Meta:
        model = models.FarmerOrders
        fields = (
            'id', 'items', 'farmer', 'distributer', 'date', 'comment',
            'status', 'totalCost'
        )

        read_only_fields = ('id',)

    # def update(self, instance, validated_data):
    #     instance.farmer = validated_data.get('farmer', instance.farmer)
    #     instance.distributer = validated_data.get('distributer', instance.distributer)
    #     instance.comment = validated_data.get('comment', instance.comment)
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.totalCost = validated_data.get('totalCost', instance.totalCost)
    #     instance.items = validated_data.get('items', instance.items)
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
            'id', 'items', 'farmer', 'distributer', 'date', 'comment', 'payment_status',
            'status', 'totalCost'
        )

        read_only_fields = ('id',)


class CRUDCartItem(serializers.ModelSerializer):
    class Meta:
        model = models.CartItems
        fields = ('id', 'item', 'quantity')
