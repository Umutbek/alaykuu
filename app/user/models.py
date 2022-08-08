import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin

from django_fsm import FSMIntegerField
import requests
from core import imggenerate
from user import utils


class City(models.Model):
    """Model for Cities"""
    nameEn = models.CharField(max_length=200, null=True, verbose_name="Название на английском")
    nameRus = models.CharField(max_length=200, null=True, verbose_name="Название на русском")
    nameKg = models.CharField(max_length=200, null=True, verbose_name="Название на кыргызком")

    def __str__(self):
        return self.nameRus

    class Meta:
        ordering = ('id',)
        verbose_name = ("Город")
        verbose_name_plural = ("Города")


class District(models.Model):
    """Model for districts"""
    nameEn = models.CharField(max_length=200, null=True, verbose_name="Название на английском")
    nameRus = models.CharField(max_length=200, null=True, verbose_name="Название на русском")
    nameKg = models.CharField(max_length=200, null=True, verbose_name="Название на кыргызком")
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, verbose_name="Город")

    def __str__(self):
        return self.nameRus

    class Meta:
        ordering = ('id',)
        verbose_name = ("Область")
        verbose_name_plural = ("Области")


class UserManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, login, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not login:
            raise ValueError('User must have an Email or Phone')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password):
        """create a superuser"""
        user = self.create_user(login, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Model for user"""
    fullname = models.CharField(max_length=200, verbose_name="Название")
    login = models.CharField(max_length=200, unique=True, verbose_name="Логин")
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name="Телефон номер")
    avatar = models.ImageField(null=True, blank=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")
    passport_front = models.ImageField(null=True, blank=True, upload_to=imggenerate.all_image_file_path, verbose_name="Паспорт лицовая сторона")
    passport_back = models.ImageField(null=True, blank=True, upload_to=imggenerate.all_image_file_path, verbose_name="Паспорт оборотная сторона")
    passport_text = models.CharField(max_length=200, null=True, blank=True, verbose_name="Паспорт номер")
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Город", related_name="farmer_city")
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Город", related_name="farmer_district")
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name="Адресс")
    comment = models.CharField(max_length=200, null=True, blank=True, verbose_name="Комментарии")
    active = models.BooleanField(default=False, verbose_name="Актив?")
    rating = models.FloatField(default=0, verbose_name="Рейтинг")
    type = FSMIntegerField(choices=utils.UserTypes.choices, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'login'


class CompanyUser(User):
    """Model for regular account"""
    access_level = models.IntegerField(default=0, verbose_name="Доступ")

    def save(self):
        if self.type == None:
            self.type = 1
        else:
            pass
        super(CompanyUser, self).save()

    class Meta:
        verbose_name = ("Пользователь")
        verbose_name_plural = ("Пользователи")