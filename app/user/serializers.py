from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate, password_validation
from django_filters import rest_framework as filters
User = get_user_model()
from rest_framework.authtoken.models import Token
from user import models
from farmer.models import Farmer
from distributer.models import Distributer


class AllUserSerializer(serializers.ModelSerializer):
    """Serializer for all users"""

    class Meta:
        model = models.User
        fields = ('id', 'fullname', 'login', 'phone', 'type')


class CompanyUserSerializer(serializers.ModelSerializer):
    """Serializer for company user"""

    class Meta:
        model = models.CompanyUser
        fields = ('id', 'fullname', 'login', 'phone', 'access_level', 'type', 'password')

        extra_kwargs = {'password':{'write_only':True},}
        read_only_fields = ('id',)


    def create(self, validated_data):
        """Create user with encrypted password and return it"""
        user = models.CompanyUser.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class FarmerSerializer(serializers.ModelSerializer):
    """Serializer for farmer"""

    class Meta:
        model = Farmer
        fields = ('id', 'fullname', 'login', 'phone', 'avatar', 'passport_front', 'passport_back',
                  'passport_text', 'city', 'district', 'address', 'comment', 'active', 'rating', 'longitude', 'latitude',
                  'verified', 'payment_left', 'type', 'password'
                  )

        extra_kwargs = {'password':{'write_only':True},}
        read_only_fields = ('id',)


    def create(self, validated_data):
        """Create user with encrypted password and return it"""
        user = Farmer.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.type = 2
        user.save()
        return user


class DistributerSerializer(serializers.ModelSerializer):
    """Serializer for distributer"""

    class Meta:
        model = Distributer
        fields = ('id', 'fullname', 'login', 'phone', 'avatar', 'passport_front', 'passport_back', 'type',
                  'passport_text', 'city', 'district', 'address', 'comment', 'active', 'rating', 'type', 'password'
                  )
        extra_kwargs = {'password':{'write_only':True},}

        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create user with encrypted password and return it"""
        user = Distributer.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    """Serializer for login"""
    login = serializers.CharField()
    password = serializers.CharField(
        style = {'input_type':'password'}, trim_whitespace=False
    )

    class Meta:
        model: User
        fields = ('login', 'password')


    def validate(self, data):
        login = data.get('login')
        password = data.get('password')

        if login is None:
            raise serializers.ValidationError(
                'A phone or email is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(
            request = self.context.get('request'),
            login=login,
            password=password,
        )

        if not user:
            msg = ('Неправильный логин или пароль')
            raise serializers.ValidationError({'detail': msg}, code='authorization')

        data['user']= user

        return data