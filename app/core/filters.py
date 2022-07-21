from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from django_filters import rest_framework as filters
from core import models
from django.db.models import Q


class ItemFilter(FilterSet):
    """Filter for an item"""
    issale = filters.CharFilter('issale')
    issale = filters.CharFilter('issale')

    min_cost= filters.CharFilter(field_name="cost",lookup_expr='gte')
    max_cost= filters.CharFilter(field_name="cost",lookup_expr='lte')

    class Meta:
        models = models.Item
        fields = ('min_cost', 'max_cost', 'issale')