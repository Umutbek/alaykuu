from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from django_filters import rest_framework as filters
from farmer import models
from django.db.models import Q


class OrderFilter(FilterSet):
    """Filter for an order"""
    farmer = filters.CharFilter('farmer')
    distributer = filters.CharFilter('distributer')
    status = filters.CharFilter('status')
    start_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = filters.DateFilter(field_name="date", lookup_expr='lte')

    class Meta:
        models = models.FarmerOrders
        fields = ('farmer', 'distributer', 'status', 'start_date', 'end_date')