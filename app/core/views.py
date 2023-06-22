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
from datetime import datetime
import requests


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, action
import requests
from website.models import WebProducts
from farmer.models import SaleFarmerCategory, SaleFarmerItem


class ItemViewSet(viewsets.ModelViewSet):
    """Manage item"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class AcceptedViewSet(viewsets.ModelViewSet):
    """Manage accepted products"""
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
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
    permission_classes = (permissions.IsAuthenticated, )
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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class MessagesViewSet(viewsets.ModelViewSet):
    """Manage messages"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = models.Messages.objects.all()
    serializer_class = serializers.MessagesSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class VideoViewSet(viewsets.ModelViewSet):
    """Manage videos"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = models.Video.objects.all()
    serializer_class = serializers.VideoSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class SliderViewSet(viewsets.ModelViewSet):
    """Manage slider"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = models.Slider.objects.all()
    serializer_class = serializers.SliderSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-priority')


class WebProductsViewSet(viewsets.ModelViewSet):
    """Manage slider"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = WebProducts.objects.all()
    serializer_class = serializers.WebProductsSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class SaleFarmerCategoryViewSet(viewsets.ModelViewSet):
    """Manage slider"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = SaleFarmerCategory.objects.all()
    serializer_class = serializers.SaleFarmerCategorySerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class SaleFarmerItemViewSet(viewsets.ModelViewSet):
    """Manage slider"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = SaleFarmerItem.objects.all()
    serializer_class = serializers.SaleFarmerItemSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.SaleFarmerItemFilter

    search_fields = ('name', 'description')

    def get_queryset(self):
        return self.queryset.all().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.SaleFarmerItemSerializerGet
        return serializers.SaleFarmerItemSerializer


class SyncWithOneCViewSet(APIView):
    authentication_classes = []

    def post(self, request):
        accepted_products_id = request.data['accepted_products']
        response_data = []
        for i in accepted_products_id:
            accepted_product = models.Accepted.objects.filter(pk=i['id']).first()
            if accepted_product.ref is None:
                if accepted_product.unit == 2:
                    dimension = 0
                else:
                    dimension = 1

                if accepted_product.status == 1:
                    payment_status = True
                else:
                    payment_status = False

                current_datetime = datetime.now()
                accepted_date = accepted_product.date
                formatted_current_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S')
                if accepted_product.date is None or accepted_product.date == "":
                    formatted_accepted_date = formatted_current_datetime
                else:
                    formatted_accepted_date = accepted_date.strftime('%Y-%m-%dT%H:%M:%S')

                auth_username = 'Администратор'
                auth_password = ''


                send_data = {
                    "Date": f"{formatted_current_datetime}",
                    "Поставщик": f"{accepted_product.farmer.oneC_id}",
                    "Контрагент": f"{accepted_product.distributor.oneC_id}",
                    "ПодотчетноеЛицо": "a6b90ec0-0ff9-11ee-99b3-e0d55eb23d4f",
                    "Организации": "f9232d18-0ff4-11ee-99b3-e0d55eb23d4f",
                    "Валюта": 417,
                    "ФормаОплаты": 0,
                    "Комментарий": f"{accepted_product.comment}",
                    "TabularSection": [
                        {
                            "Номенклатура": f"{accepted_product.item.oneC_id}",
                            "Количество": accepted_product.amount,
                            "Измерение": dimension,
                            "Цена": accepted_product.item.cost,
                            "Скидка": 0,
                            "ОбшаяСумма": accepted_product.totalCost,
                            "ДатаОплаты": f"{formatted_accepted_date}",
                            "СтатусОплаты": payment_status
                        }
                    ]
                }

                oneC_request = requests.post('http://212.42.107.229/alayku/hs/exchange/document/purchase/',
                                             json=send_data, auth=(auth_username, auth_password))
                response_data.append(oneC_request.json())
            else:
                message = {"message": f"The ref model field of the accepted product with this ID exists ({i['id']})"}
                response_data.append(message)
        return Response({'response': response_data})
