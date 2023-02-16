from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status, permissions, generics
from django.shortcuts import redirect
from core import models, serializers, filters
from django.views.generic import TemplateView
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import FilterSet

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, action
import requests
from website.models import WebProducts
from farmer.models import SaleFarmerCategory, SaleFarmerItem


class ItemViewSet(viewsets.ModelViewSet):
    """Manage item"""
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class AcceptedViewSet(viewsets.ModelViewSet):
    """Manage accepted products"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    queryset = models.Accepted.objects.all()
    serializer_class = serializers.AcceptedSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.AcceptedProductsFilter
    search_fields = ('item__name',)

    ordering_fields = ('farmer', 'distributer')

    def get_queryset(self):
        return self.queryset.all().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.GetAcceptedSerializer
        return serializers.AcceptedSerializer

    def create(self, request, *args, **kwargs):
        serializer = serializers.AcceptedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved_data = serializer.save()

        return Response(serializer.data)


class PaymentViewSet(viewsets.ModelViewSet):
    """Manage accepted products"""
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.PaymentFilter

    def get_queryset(self):
        return self.queryset.all().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.PaymentSerializerGet
        return serializers.PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = serializers.PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved_data = serializer.save()
        payment = models.Payment.objects.get(pk=serializer.data['id'])
        farmer = models.Farmer.objects.filter(id=payment.farmer.id).first()
        farmer.payment_left = farmer.payment_left - payment.totalCost
        if farmer.payment_left < 0:
            farmer.payment_left = 0
        farmer.save()
        products = request.data['products']
        for i in products:
            prods = models.Accepted.objects.get(pk=i)
            prods.status = 1
            prods.save()
        return Response(serializer.data)


class NewsViewSet(viewsets.ModelViewSet):
    """Manage news"""
    queryset = models.News.objects.all()
    serializer_class = serializers.NewsSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class JobsViewSet(viewsets.ModelViewSet):
    """Manage jobs"""
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class MessagesViewSet(viewsets.ModelViewSet):
    """Manage messages"""
    queryset = models.Messages.objects.all()
    serializer_class = serializers.MessagesSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class VideoViewSet(viewsets.ModelViewSet):
    """Manage videos"""
    queryset = models.Video.objects.all()
    serializer_class = serializers.VideoSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class SliderViewSet(viewsets.ModelViewSet):
    """Manage slider"""
    queryset = models.Slider.objects.all()
    serializer_class = serializers.SliderSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-priority')


class WebProductsViewSet(viewsets.ModelViewSet):
    """Manage slider"""
    queryset = WebProducts.objects.all()
    serializer_class = serializers.WebProductsSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class SaleFarmerCategoryViewSet(viewsets.ModelViewSet):
    """Manage slider"""
    queryset = SaleFarmerCategory.objects.all()
    serializer_class = serializers.SaleFarmerCategorySerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class SaleFarmerItemViewSet(viewsets.ModelViewSet):
    """Manage slider"""
    queryset = SaleFarmerItem.objects.all()
    serializer_class = serializers.SaleFarmerItemSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter)

    search_fields = ('name', 'description')

    def get_queryset(self):
        return self.queryset.all().order_by('-id')