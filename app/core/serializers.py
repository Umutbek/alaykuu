from rest_framework import serializers
from core import models

class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item"""

    class Meta:
        model = models.Item
        fields = (
            'id', 'name', 'image', 'image', 'unit', 'type', 'amountleft', 'issale', 'cost',
            'costSale'
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


class AcceptedSerializer(serializers.ModelSerializer):
    """Serializer for accepted product"""

    class Meta:
        model = models.Accepted
        fields = (
            'id', 'item', 'farmer', 'distributor', 'amount', 'unit', 'unitCost', 'discount', 'totalCost',
            'status', 'comment', 'sort', 'fat', 'acidity'
            )

        read_only_fields = ('id',)


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment"""

    class Meta:
        model = models.Payment
        fields = (
            'id', 'date', 'farmer', 'totalCost', 'comment'
            )

        read_only_fields = ('id', 'date')


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
            'id', 'date', 'video'
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
