# -*- coding: utf-8 -*-
import random

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status, permissions, generics, authentication
from django.shortcuts import redirect
from rest_framework_simplejwt.authentication import JWTAuthentication

from farmer import filters
from user import models, serializers
from django.views.generic import TemplateView
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import FilterSet
from rest_framework.authtoken.models import Token

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, action
from django_filters import DateFilter
import requests
from farmer.models import Farmer, ModelCows
from distributer.models import Distributer
from laborant.models import LaborantUser
from user.models import User
from user.serializers import PasswordResetRequestSerializer, PasswordResetRequestResponse, PasswordResetSerializer, \
    PasswordResetResponse
from rest_framework_simplejwt.tokens import RefreshToken


class CompanyUserViewSet(viewsets.ModelViewSet):
    """Manage Store"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.CompanyUser.objects.all()
    serializer_class = serializers.CompanyUserSerializer

    pagination_class = None


class FarmerViewSet(viewsets.ModelViewSet):
    """Manage Farmers"""
    permission_classes = (permissions.AllowAny,)
    queryset = Farmer.objects.all()
    serializer_class = serializers.FarmerSerializer
    pagination_class = None
    search_fields = ('fullname',)

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.FarmerFilters

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        cows = request.data['cows']
        cows_id = []
        if cows:
            for i in cows:
                cow = ModelCows.objects.create(**i)
                cows_id.append(cow.id)

        request.data['cows'] = cows_id
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class DistributerViewSet(viewsets.ModelViewSet):
    """Manage Distributers"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Distributer.objects.all()
    serializer_class = serializers.DistributerSerializer
    pagination_class = None


class LaborantViewSet(viewsets.ModelViewSet):
    """Manage Laborant"""
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = LaborantUser.objects.all()
    serializer_class = serializers.LaborantSerializer
    pagination_class = None


class GetMeView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = serializers.AllUserSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user


from rest_framework_simplejwt.tokens import RefreshToken


class LoginAPI(APIView):
    """Create a new auth token for user"""
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        info = models.User.objects.filter(login=user)
        userdata = serializers.AllUserSerializer(info, many=True)
        refresh = RefreshToken.for_user(user)
        # token, created = Token.objects.get_or_create(user=user)
        return Response({"refresh": str(refresh),
                         "access": str(refresh.access_token),
                        'data': userdata.data}, status=200)


class CityViewSet(viewsets.ModelViewSet):
    """Manage city"""
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerializer
    pagination_class = None


class DistrictViewSet(viewsets.ModelViewSet):
    """Manage user district"""
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.District.objects.all()
    serializer_class = serializers.DistrictSerializer
    pagination_class = None


class OneCUserViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = models.Model1CUser.objects.all()
    serializer_class = serializers.OneCUserSerializer
    pagination_class = None


class RequestPasswordResetView(APIView):
    permission_classes = (permissions.AllowAny, )

    @swagger_auto_schema(request_body=PasswordResetRequestSerializer(), responses={200: PasswordResetRequestResponse()})
    def post(self, request, format=None):
        serializer = serializers.PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recovery_email = serializer.validated_data.get('email')
        user = User.objects.filter(login=recovery_email).first()
        if not user:
            raise ValidationError({'email': ['Пользователя с этой почтой не существует!']})

        code = random.randint(100_000, 999_999)
        while User.objects.filter(reset_code=code).exists():
            code = random.randint(100_000, 999_999)
        user.reset_code = code
        from django.conf import settings
        from django.core.mail import send_mail
        from django.utils.encoding import smart_str

        message = smart_str(f'Code: {user.reset_code}')
        send_mail(
            subject='Password reset!',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recovery_email],
            fail_silently=False,
        )
        user.save()
        return Response(PasswordResetRequestResponse({"message": "OK"}).data)


class ValidateResetCodeView(APIView):
    permission_classes = (permissions.AllowAny, )

    @swagger_auto_schema(request_body=PasswordResetSerializer(), responses={200: PasswordResetResponse()})
    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        user = User.objects.filter(reset_code=code).first()
        error = ValidationError({'code': ['Неверный код']})
        if not user:
            raise error
        if user.reset_code == code:
            user.reset_code = ''
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response(PasswordResetResponse({
                'token': refresh.access_token,
                'data': user.id,
            }).data)
        else:
            raise error


class ChangePasswordWithoutOldPasswordView(generics.UpdateAPIView):
    serializer_class = serializers.ChangePasswordWithoutOldPasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user_id = User.objects.get(pk=serializer.data.get('user_id'))
            self.object = user_id
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
