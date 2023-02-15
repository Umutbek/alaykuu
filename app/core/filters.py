from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from django_filters import rest_framework as filters
from core import models
from django.db.models import Q


class ItemFilter(FilterSet):
    """Filter for an item"""
    issale = filters.CharFilter('issale')
    min_cost= filters.CharFilter(field_name="cost",lookup_expr='gte')
    max_cost= filters.CharFilter(field_name="cost",lookup_expr='lte')

    class Meta:
        models = models.Item
        fields = ('min_cost', 'max_cost', 'issale')


class AcceptedProductsFilter(FilterSet):
    """Filter for an item"""
    farmer = filters.CharFilter('farmer')
    distributor = filters.CharFilter('distributor')
    status = filters.CharFilter('status')
    sort = filters.CharFilter('sort')
    start_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = filters.DateFilter(field_name="date", lookup_expr='lte')

    class Meta:
        models = models.Accepted
        fields = ('farmer', 'distributor', 'sort', 'status', 'start_date', 'end_date')
