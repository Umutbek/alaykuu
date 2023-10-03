from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from django_filters import rest_framework as filters
from core import models
from django.db.models import Q
from farmer.models import SaleFarmerItem


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
    gte_fat = filters.CharFilter(field_name='fat', lookup_expr='gte')
    lte_fat = filters.CharFilter(field_name='fat', lookup_expr='lte')
    payment_type = filters.CharFilter('payment_type')
    probnik_gt = filters.CharFilter(field_name='probnik', lookup_expr='gt')

    class Meta:
        models = models.Accepted
        fields = ('farmer', 'distributor', 'sort', 'status', 'start_date', 'end_date', 'gte_fat', 'lte_fat',
                  'payment_type', 'probnik_gt'
                                  '')


class PaymentFilter(FilterSet):
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte')
    district = filters.CharFilter('district')
    farmer = filters.CharFilter('farmer')

    class Meta:
        models = models.Payment
        fields = ('start_date', 'end_date', 'farmer', 'district')


class SaleFarmerItemFilter(FilterSet):
    districts = filters.ModelMultipleChoiceFilter(queryset=models.District.objects.all())

    class Meta:
        models = SaleFarmerItem
        fields = ('districts', )
