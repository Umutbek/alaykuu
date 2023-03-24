from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status, permissions, generics, authentication
from django.shortcuts import redirect

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
from farmer.models import Farmer
from distributer.models import Distributer
from  laborant.models import LaborantUser


class CompanyUserViewSet(viewsets.ModelViewSet):
    """Manage Store"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.CompanyUser.objects.all()
    serializer_class = serializers.CompanyUserSerializer

    pagination_class = None


class FarmerViewSet(viewsets.ModelViewSet):
    """Manage Farmers"""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Farmer.objects.all()
    serializer_class = serializers.FarmerSerializer
    pagination_class = None
    search_fields = ('fullname',)

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.FarmerFilters


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
