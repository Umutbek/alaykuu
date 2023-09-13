from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate, password_validation
from django_filters import rest_framework as filters
User = get_user_model()
from rest_framework.authtoken.models import Token
from user import models
from farmer.models import Farmer, ModelCows
from distributer.models import Distributer
from  laborant.models import LaborantUser


class AllUserSerializer(serializers.ModelSerializer):
    """Serializer for all users"""

    class Meta:
        model = models.User
        fields = ('id', 'fullname', 'login', 'phone', 'type', 'active')


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


class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelCows
        fields = ('cow_id', )
        # read_only_fields = ('id', )


class FarmerSerializer(serializers.ModelSerializer):
    """Serializer for farmer"""
    cows = CowSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Farmer
        fields = ('id', 'fullname', 'login', 'phone', 'avatar', 'passport_front', 'passport_back', 'cows',
                  'passport_text', 'city', 'district', 'address', 'comment', 'farmer_type', 'active', 'rating', 'longitude', 'latitude',
                  'verified', 'payment_left', 'type', 'password', 'oneC_id', 'milkCost', 'paymentType', 'cardNumber'
                  )

        extra_kwargs = {'password': {'write_only': True}, }
        read_only_fields = ('id', )

    def create(self, validated_data):
        """Create user with encrypted password and return it"""
        cows = validated_data.pop('cows', None)
        cows_id = []
        if cows:
            for i in cows:
                cow = ModelCows.objects.create(**i)
                cows_id.append(cow.id)
        user = Farmer.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.type = 2
        user.save()
        for i in cows_id:
            user.cows.add(i)
        user.save()
        return user

    def update(self, instance, validated_data):
        cows = validated_data['cows']
        if cows:
            instance.cows = None
            instance.save()
            for i in cows:
                cow = ModelCows.objects.create(**i)
                instance.cows.add(cow.id)
        instance.save()
        return instance

class DistributerSerializer(serializers.ModelSerializer):
    """Serializer for distributer"""

    class Meta:
        model = Distributer
        fields = ('id', 'fullname', 'login', 'phone', 'avatar', 'passport_front', 'passport_back', 'type',
                  'passport_text', 'city', 'district', 'address', 'comment', 'active', 'rating', 'type', 'password',
                  'oneC_id'
                  )
        extra_kwargs = {'password':{'write_only':True},}

        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create user with encrypted password and return it"""
        user = Distributer.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LaborantSerializer(serializers.ModelSerializer):
    """Serializer for "laborant"""

    class Meta:
        model = LaborantUser
        fields = ('id', 'fullname', 'login', 'phone', 'avatar', 'passport_front', 'passport_back', 'type',
                  'passport_text', 'city', 'district', 'address', 'comment', 'active', 'rating', 'type', 'password'
                  )
        extra_kwargs = {'password':{'write_only':True},}

        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create user with encrypted password and return it"""
        user = LaborantUser.objects.create_user(**validated_data)
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

        print(data['user'].type)

        return data


class CitySerializer(serializers.ModelSerializer):
    """Serializer for city"""

    class Meta:
        model = models.City
        fields = ('id', 'nameEn', 'nameRus', 'nameKg')


class DistrictSerializer(serializers.ModelSerializer):
    """Serializer for district"""

    class Meta:
        model = models.District
        fields = ('id', 'nameEn', 'nameRus', 'nameKg', 'city', 'oneC_id', 'milkCost')


class OneCUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model1CUser
        fields = ('id', 'fullname', 'name', 'login', 'password', 'type')
        extra_kwargs = {'password':{'write_only':True},}

        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create user with encrypted password and return it"""
        user = models.Model1CUser.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ('email', )


class PasswordResetRequestResponse(serializers.Serializer):
    message = serializers.CharField(max_length=2)

    class Meta:
        fields = ('message', )


class PasswordResetSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    class Meta:
        fields = ('code', )


class PasswordResetResponse(serializers.Serializer):
    token = serializers.CharField(max_length=50)
    data = serializers.IntegerField(help_text='User ID')

    class Meta:
        fields = ('token', 'data')


class ChangePasswordWithoutOldPasswordSerializer(serializers.Serializer):
    models = User

    new_password = serializers.CharField(required=True)
    user_id = serializers.CharField(required=True)
