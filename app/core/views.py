import base64

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status, permissions, generics
from django.shortcuts import redirect
from rest_framework_simplejwt.authentication import JWTAuthentication

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

from core.serializers import SetFatSerializer, ChangeCostSerializer
from farmer.utils import MilkCostConst
from website.models import WebProducts
from farmer.models import SaleFarmerCategory, SaleFarmerItem


class ItemViewSet(viewsets.ModelViewSet):
    """Manage item"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class AcceptedViewSet(viewsets.ModelViewSet):
    """Manage accepted products"""
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_data = self.perform_update(serializer)
        product = self.get_object()
        new_milk_cost = 0
        # if product.probnik > 0 and product.probnik < 3.4:
        #     minus_num = product.probnik
        #     if minus_num < 3.4 and minus_num > 2.4:
        #         product.unitCost = product.farmer.milkCost - 0.5
        #     elif minus_num <= 2.4 and minus_num > 1.4:
        #         product.unitCost = product.farmer.milkCost - 1
        #     elif minus_num <= 1.4 and minus_num > 0.4:
        #         product.unitCost = product.farmer.milkCost - 1.5
        #     elif minus_num <= 0.4 and minus_num > 0:
        #         product.unitCost = product.farmer.milkCost - 2
        # else:
        #     if product.probnik == 0:
        #         if product.fat > 0 and product.fat < 3.4:
        #             minus_num = product.fat
        #             if minus_num < 3.4 and minus_num > 2.4:
        #                 product.unitCost = product.farmer.milkCost - 0.5
        #             elif minus_num <= 2.4 and minus_num > 1.4:
        #                 product.unitCost = product.farmer.milkCost - 1
        #             elif minus_num <= 1.4 and minus_num > 0.4:
        #                 product.unitCost = product.farmer.milkCost - 1.5
        #             elif minus_num <= 0.4 and minus_num > 0:
        #                 product.unitCost = product.farmer.milkCost - 2
        #     else:
        #         product.unitCost = product.Farmer.milkCost

        if product.probnik >= 3.4 or product.fat >= 3.4:
            product.unitCost = product.farmer.milkCost
        elif product.probnik > 0 and product.probnik < 3.4:
            minus_num = product.probnik
            product.unitCost = product.farmer.milkCost - (5 * (3.4 - minus_num))

            # if minus_num < 3.4 and minus_num > 2.4:
            #     product.unitCost = product.farmer.milkCost - 0.5
            # elif minus_num <= 2.4 and minus_num > 1.4:
            #     product.unitCost = product.farmer.milkCost - 1
            # elif minus_num <= 1.4 and minus_num > 0.4:
            #     product.unitCost = product.farmer.milkCost - 1.5
            # elif minus_num <= 0.4 and minus_num > 0:
            #     product.unitCost = product.farmer.milkCost - 2
        else:
            if product.probnik == 0:
                if product.fat > 0 and product.fat < 3.4:
                    minus_num = product.fat
                    product.unitCost = product.farmer.milkCost - (5 * (3.4 - minus_num))
                    # if minus_num < 3.4 and minus_num > 2.4:
                    #     product.unitCost = product.farmer.milkCost - 0.5
                    # elif minus_num <= 2.4 and minus_num > 1.4:
                    #     product.unitCost = product.farmer.milkCost - 1
                    # elif minus_num <= 1.4 and minus_num > 0.4:
                    #     product.unitCost = product.farmer.milkCost - 1.5
                    # elif minus_num <= 0.4 and minus_num > 0:
                    #     product.unitCost = product.farmer.milkCost - 2
        product.totalCost = product.amount * product.unitCost
        product.save()

        # if product.fat < 3.4 and product.fat > 0 and product.probnik == 0:
        #     new_milk_cost = MilkCostConst - ((3.4 - product.fat) * 10 * 0.5)
        # else:
        #     if product.fat == 0 and product.probnik > 0 and product.probnik < 3.4:
        #         new_milk_cost = MilkCostConst - ((3.4 - product.probnik) * 10 * 0.5)
        # if new_milk_cost:
        #     district_id = product.farmer.district_id
        #     farmers = models.Farmer.objects.filter(district_id=district_id)
        #     for i in farmers:
        #         i.milkCost = new_milk_cost
        #         i.save()
        return Response(serializer.data)


class PaymentViewSet(viewsets.ModelViewSet):
    """Manage accepted products"""
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.PaymentFilter
    search_fields = ('farmer__fullname',)

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class MessagesViewSet(viewsets.ModelViewSet):
    """Manage messages"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Messages.objects.all()
    serializer_class = serializers.MessagesSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class VideoViewSet(viewsets.ModelViewSet):
    """Manage videos"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Video.objects.all()
    serializer_class = serializers.VideoSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class SliderViewSet(viewsets.ModelViewSet):
    """Manage slider"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Slider.objects.all()
    serializer_class = serializers.SliderSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-priority')


class WebProductsViewSet(viewsets.ModelViewSet):
    """Manage slider"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = WebProducts.objects.all()
    serializer_class = serializers.WebProductsSerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class SaleFarmerCategoryViewSet(viewsets.ModelViewSet):
    """Manage slider"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = SaleFarmerCategory.objects.all()
    serializer_class = serializers.SaleFarmerCategorySerializer

    def get_queryset(self):
        return self.queryset.all().order_by('-id')


class SaleFarmerItemViewSet(viewsets.ModelViewSet):
    """Manage slider"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
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


import json


def remove_bom_from_json(json_data):
    json_text = json_data.decode('utf-8-sig')  # Декодируем текст в кодировке UTF-8-sig, удаляя BOM символы
    json_object = json.loads(json_text)  # Преобразуем текст JSON в объект Python
    return json_object


def remove_bom(data):
    bom_chars = [b'\xef\xbb\xbf', b'\xff\xfe']  # UTF-8 и UTF-16 BOM символы

    for bom in bom_chars:
        if data.startswith(bom):
            data = data[len(bom):]
            break

    return data


class SyncWithOneCViewSet(APIView):
    authentication_classes = []

    def post(self, request):
        accepted_products_id = request.data['accepted_products']
        response_data = []
        for i in accepted_products_id:
            accepted_product = models.Accepted.objects.filter(pk=i['id']).first()
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

            credentials = base64.b64encode(f"{auth_username}:{auth_password}".encode('utf-8')).decode('utf-8')

            headers = {
                'Authorization': f'Basic {credentials}'
            }
            if accepted_product.ref:
                refchik = accepted_product.ref
            else:
                refchik = ''

            pay_stat = False
            if accepted_product.status == 1:
                pay_stat = True

            send_data = {
                "Date": f"{formatted_accepted_date}",
                "Ref": f'{refchik}',
                "Поставщик": "7b5ab912-d38e-11ed-997d-e0d55eb23d4f",
                "Контрагент": "7b5ab916-d38e-11ed-997d-e0d55eb23d4f",
                "Организация": "07db7fcf-82b0-11ed-8480-107b4492ed8b",
                "Склад": "deb552c8-8698-11ed-8481-107b4492ed8b",
                "Подразделение": "bf43d16c-93bc-11ed-964d-fc3497beb46e",
                "Менеджер": "8c6ed3fc-85d9-11ed-8481-107b4492ed8b",
                "СуммаДокумента": 59,
                "Валюта": "417",
                "ФормаОплаты": 0,
                "Комментарий": "sa",
                "TabularSection": [
                    {
                        "Номенклатура": "bcbdff43-8504-11ed-8480-107b4492ed8b",
                        "Количество": accepted_product.amount,
                        "Измерение": 0,
                        "Цена": accepted_product.unitCost,
                        "Скидка": 0,
                        "ОбшаяСумма": accepted_product.totalCost,
                        "ДатаОплаты": f"{formatted_current_datetime}",
                        "Характеристика": "Цельное, л",
                        "СтатусОплаты": pay_stat
                    }
                ]
            }

            send_data_json = json.dumps(send_data)  # Преобразование словаря send_data в JSON строку
            send_data_json_bytes = send_data_json.encode('utf-8')  # Кодирование JSON строки в байты

            send_data_json_bytes_without_bom = remove_bom(send_data_json_bytes)  # Удаление BOM символов из данных

            send_data_without_bom = json.loads(
                send_data_json_bytes_without_bom.decode('utf-8'))  # Преобразование данных в объект Python

            oneC_request = requests.post('http://84.46.242.63/alayku_cndb/hs/DataExchange/document/purchase',
                                         json=send_data_without_bom, headers=headers)

            response_data.append(oneC_request.json())
            ref = oneC_request.json()['Ref']
            accepted_product.ref = ref
            accepted_product.status = 1
            accepted_product.save()
        return Response({'response': response_data})


class ImagesViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Images.objects.all()
    serializer_class = serializers.ImagesSerializer
    pagination_class = None


class SetFatViewSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(request_body=SetFatSerializer())
    def post(self, request):
        items = request.data['items']
        fat = request.data['fat']
        data = []
        for item in items:
            product = models.Accepted.objects.filter(pk=item).first()
            if product:
                product.fat = fat
                product.save()
                if product.probnik >= 3.4 or product.fat >= 3.4:
                    product.unitCost = product.farmer.milkCost
                elif product.probnik > 0 and product.probnik < 3.4:
                    minus_num = product.probnik
                    product.unitCost = product.farmer.milkCost - (5 * (3.4 - minus_num))
                    # if minus_num < 3.4 and minus_num > 2.4:
                    #     product.unitCost = product.farmer.milkCost - 0.5
                    # elif minus_num <= 2.4 and minus_num > 1.4:
                    #     product.unitCost = product.farmer.milkCost - 1
                    # elif minus_num <= 1.4 and minus_num > 0.4:
                    #     product.unitCost = product.farmer.milkCost - 1.5
                    # elif minus_num <= 0.4 and minus_num > 0:
                    #     product.unitCost = product.farmer.milkCost - 2
                else:
                    if product.probnik == 0:
                        if product.fat > 0 and product.fat < 3.4:
                            minus_num = product.fat
                            product.unitCost = product.farmer.milkCost - (5 * (3.4 - minus_num))
                            # if minus_num < 3.4 and minus_num > 2.4:
                            #     product.unitCost = product.farmer.milkCost - 0.5
                            # elif minus_num <= 2.4 and minus_num > 1.4:
                            #     product.unitCost = product.farmer.milkCost - 1
                            # elif minus_num <= 1.4 and minus_num > 0.4:
                            #     product.unitCost = product.farmer.milkCost - 1.5
                            # elif minus_num <= 0.4 and minus_num > 0:
                            #     product.unitCost = product.farmer.milkCost - 2
                product.totalCost = product.amount * product.unitCost
                product.save()
                data.append({'items': product.id})

        return Response({'success': data})


class ChangeCostViewSet(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=ChangeCostSerializer())
    def post(self, request, format=None):
        serializer = serializers.ChangeCostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        accepted = models.Accepted.objects.filter(pk=serializer.validated_data['id']).first()
        accepted.unitCost = serializer.validated_data['unitCost']
        accepted.totalCost = serializer.validated_data['totalCost']
        accepted.save()
        return Response({'status': 'ok'})
