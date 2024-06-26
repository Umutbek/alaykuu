from rest_framework import serializers
from core import models
from website.models import WebProducts
from farmer.models import SaleFarmerCategory, SaleFarmerItem
from user.serializers import FarmerSerializer, DistributerSerializer, DistrictSerializer


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item"""

    class Meta:
        model = models.Item
        fields = (
            'id', 'name', 'image', 'image', 'unit', 'type', 'amountleft', 'issale', 'cost',
            'costSale', 'oneC_id'
            )

        read_only_fields = ('id',)


class SortSerializer(serializers.ModelSerializer):
    """Serializer for Sort"""

    class Meta:
        model = models.Sort
        fields = (
            'id', 'name'
            )

        read_only_fields = ('id',)


class GetAcceptedSerializer(serializers.ModelSerializer):
    """ Get Serializer for accepted product"""
    farmer = FarmerSerializer()
    distributor = DistributerSerializer()
    item = ItemSerializer()

    class Meta:
        model = models.Accepted
        fields = (
            'id', 'item', 'farmer', 'distributor', 'amount', 'unit', 'unitCost', 'discount', 'totalCost', 'status',
            'comment', 'sort', 'fat', 'acidity', 'date', 'date_second', 'payment_method', 'payment_type', 'ref',
            'sync_with_oneC', 'farmerReview', 'farmerComment', 'probnik'
            )

        read_only_fields = ('id', )


class AcceptedSerializer(serializers.ModelSerializer):
    """Serializer for accepted product"""

    class Meta:
        model = models.Accepted
        fields = (
            'id', 'item', 'farmer', 'distributor', 'amount', 'unit', 'unitCost', 'discount', 'totalCost', 'status',
            'comment', 'sort', 'fat', 'acidity', 'date', 'date_second', 'payment_method', 'payment_type', 'ref',
            'farmerReview', 'farmerComment', 'probnik'
            )

        read_only_fields = ('id', )

    def create(self, validated_data):
        """Create user with encrypted password and return it"""

        accepted_item = models.Accepted.objects.create(**validated_data)
        item = models.Item.objects.filter(id=accepted_item.item.id).first()

        if item:
            item.amountleft = item.amountleft + accepted_item.amount
            item.save()

        if accepted_item.status == 2:
            farmer = models.Farmer.objects.filter(id=accepted_item.farmer.id).first()
            farmer.payment_left = farmer.payment_left + accepted_item.totalCost
            farmer.save()

        accepted_item.payment_type = accepted_item.farmer.paymentType
        accepted_item.save()

        return accepted_item


    def update(self, instance, validated_data):

        instance.status = validated_data.get('status', instance.status)
        instance.item = validated_data.get('item', instance.item)
        instance.farmer = validated_data.get('farmer', instance.farmer)
        instance.distributor = validated_data.get('distributor', instance.distributor)

        instance.totalCost = validated_data.get('totalCost', instance.totalCost)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.date_second = validated_data.get('date_second', instance.date_second)

        instance.discount = validated_data.get('discount', instance.discount)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.sort = validated_data.get('sort', instance.sort)
        instance.fat = validated_data.get('fat', instance.fat)
        instance.acidity = validated_data.get('acidity', instance.acidity)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.payment_type = validated_data.get('payment_type', instance.payment_type)
        instance.probnik = validated_data.get('probnik', instance.probnik)
        instance.farmerComment = validated_data.get('farmerComment', instance.farmerComment)

        instance.save()

        if instance.status == 1:
            farmer = models.Farmer.objects.filter(id=instance.farmer.id).first()
            print("Farmer", farmer)
            farmer.payment_left = farmer.payment_left - instance.totalCost
            farmer.save()

        return instance


class PaymentSerializerGet(serializers.ModelSerializer):
    """Serializer for Payment"""
    products = AcceptedSerializer(many=True)
    farmer = FarmerSerializer()
    district = DistrictSerializer()

    class Meta:
        model = models.Payment
        fields = (
            'id', 'date', 'farmer', 'district', 'totalCost', 'comment', 'products'
            )

        read_only_fields = ('id', 'date')


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment"""

    class Meta:
        model = models.Payment
        fields = (
            'id', 'date', 'farmer', 'district', 'totalCost', 'comment', 'products'
            )

        read_only_fields = ('id', 'date')

    # def create(self, validated_data):
    #     """Create user with encrypted password and return it"""
    #
    #     payment = models.Payment.objects.create(**validated_data)
    #
    #     farmer = models.Farmer.objects.filter(id=payment.farmer.id).first()
    #     farmer.payment_left = farmer.payment_left - payment.totalCost
    #     if farmer.payment_left < 0:
    #         farmer.payment_left = 0
    #     farmer.save()
    #
    #     return payment


class NewsSerializer(serializers.ModelSerializer):
    """Serializer for news"""

    class Meta:
        model = models.News
        fields = (
            'id', 'photo', 'headline', 'text', 'date'
            )

        read_only_fields = ('id', 'date')


class JobSerializer(serializers.ModelSerializer):
    """Serializer for job"""

    class Meta:
        model = models.Job
        fields = (
            'id', 'jobtitle', 'text', 'date', 'requirements', 'responsibilities',
            'job_conditions'
            )

        read_only_fields = ('id', 'date')


class MessagesSerializer(serializers.ModelSerializer):
    """Serializer for messages"""

    class Meta:
        model = models.Messages
        fields = (
            'id', 'fullname', 'email', 'phone'
            )

    read_only_fields = ('id',)


class VideoSerializer(serializers.ModelSerializer):
    """Serializer for video"""

    class Meta:
        model = models.Video
        fields = (
            'id', 'date', 'video', 'thumbnail'
            )

        read_only_fields = ('id', 'date')


class SliderSerializer(serializers.ModelSerializer):
    """Serializer for slider"""

    class Meta:
        model = models.Slider
        fields = (
            'id', 'priority', 'photo'
        )

        read_only_fields = ('id',)


class WebProductsSerializer(serializers.ModelSerializer):
    """Serializer for web products"""

    class Meta:
        model = WebProducts
        fields = (
            'id', 'name', 'image', 'category'
        )

        read_only_fields = ('id',)


class SaleFarmerCategorySerializer(serializers.ModelSerializer):
    """Serializer for fermer's sale category serializer"""

    class Meta:
        model = SaleFarmerCategory
        fields = (
            'id', 'nameRu', 'nameKg', 'nameEn'
        )

        read_only_fields = ('id',)


class SaleFarmerItemSerializer(serializers.ModelSerializer):
    """Serializer for farmer sale products"""

    class Meta:
        model = SaleFarmerItem
        fields = (
            'id', 'name', 'image', 'category', 'cost', 'description', 'districts', 'is_sale', 'sale_cost'
        )

        read_only_fields = ('id',)


class SaleFarmerItemSerializerGet(serializers.ModelSerializer):
    """Serializer for farmer sale products"""
    districts = DistrictSerializer(many=True)

    class Meta:
        model = SaleFarmerItem
        fields = (
            'id', 'name', 'image', 'category', 'cost', 'description', 'districts', 'is_sale', 'sale_cost'
        )

        read_only_fields = ('id', )


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Images
        fields = ('id', 'title', 'image')


class SetFatSerializer(serializers.Serializer):
    items = serializers.ListSerializer(child=serializers.IntegerField(min_value=0))
    fat = serializers.FloatField()

    class Meta:
        fields = ('items', 'fat')


class ChangeCostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    unitCost = serializers.FloatField()
    totalCost = serializers.FloatField()

    class Meta:
        fields = ('id', 'unitCost', 'totalCost')
