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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.FarmerOrders.objects.all()
    serializer_class = serializers.OrderSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.OrderFilter

    def get_queryset(self):
        return self.queryset.all().order_by("-id")

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.GetOrderSerializer
        # if self.action == 'update':
        #     return serializers.OrderSerializerUpdate
        return serializers.OrderSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = serializers.OrderSerializer(data=request.data)
    #     ourItems = request.data['items']
    #     if ourItems:
    #         for i in request.data['items']:
    #             cartItems = models.CartItems.objects.create(item_id=i['item'], quantity=i['quantity'])
    #
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)


    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     order = models.FarmerOrders.objects.get(pk=instance.id)
    #     order.items = request.data['items']
    #     # items = serializer.data('items')
    #     order.save()
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #
    #     # order.cartitems_set = []
    #     # order.save()
    #     # order.cartitems_set.update(self, request.data['items'])
    #     # order.save()
    #
    #     return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = models.CartItems.objects.all()
    serializer_class = serializers.CRUDCartItem

    def create(self, request, *args, **kwargs):
        serializer = serializers.CRUDCartItem
        responseData = []
        for item in request.data['cart_items']:
            cart_item = models.CartItems.objects.create(order_id=item.get('order'), item_id=item.get('item'),
                                                        quantity=item.get('quantity'))
            cart_item.save()
            data = {
                'cartItemId': cart_item.id
            }
            responseData.append(data)
        return Response({'data': responseData}, status=status.HTTP_200_OK)
