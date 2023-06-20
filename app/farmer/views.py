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
        return serializers.OrderSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = models.CartItems.objects.all()
    serializer_class = serializers.CRUDCartItem

    def create(self, request, *args, **kwargs):
        serializer = serializers.CRUDCartItem
        responseData = []
        for item in request.data['cart_items']:
            cart_item = models.CartItems.objects.create(item_id=item.get('item'),
                                                        quantity=item.get('quantity'))
            cart_item.save()
            data = {
                'cartItemId': cart_item.id
            }
            responseData.append(data)
        return Response({'data': responseData}, status=status.HTTP_200_OK)


class CartItemsViewSet(APIView):
    authentication_classes = []

    def post(self, request):
        data = []
        for i in request.data['cart_items']:
            cart_item = models.CartItems.objects.create(item_id=i['item'], quantity=i['quantity'])
            cart_item.save()
            id = {'id': f'{cart_item.id}'}
            data.append(id)
        return Response({'data': data})
