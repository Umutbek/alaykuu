from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status, permissions, generics
from django.shortcuts import redirect
from farmer import models, serializers, filters
from django.views.generic import TemplateView
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import FilterSet
from rest_framework.authtoken.models import Token

from django.db.models import Sum, Count, F, Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, action
from django_filters import DateFilter
import requests


class OrderViewSet(viewsets.ModelViewSet):
    """API view for client order list"""
    queryset = models.FarmerOrders.objects.all()
    serializer_class = serializers.OrderSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.OrderFilter

    def get_queryset(self):
        return self.queryset.all().order_by("-id")

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.GetOrderSerializer
        return serializers.OrderSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        req_items = request.data['items']
        newItems = []
        for i in req_items:
            item = models.CartItems.objects.create(item=models.SaleFarmerItem.objects.get(pk=i['item']),
                                                   quantity=i['quantity'])
            newItems.append(item.id)
            # newItems.append({'id': item.id, 'item': item.item_id, 'quantity': item.quantity})
        # request.data['items'] = newItems
        print(request.data)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
