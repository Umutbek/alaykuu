from django.db import models
from user.models import User
from core import imggenerate
from distributer.models import Distributer
from django_fsm import FSMIntegerField
from farmer import utils
# Create your models here.


class Farmer(User):
    """Model for farmer"""
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    verified = models.BooleanField(default=False, verbose_name="Проверено?")
    payment_left = models.FloatField(null=True, blank=True, verbose_name="Оставшаяся сумма")

    def save(self):
        if self.type == None:
            self.type = 2
        else:
            pass
        super(Farmer, self).save()

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Фермер")
        verbose_name_plural = ("Фермеры")


class SaleFarmerCategory(models.Model):
    nameRu = models.CharField(max_length=500, verbose_name="Название на русском")
    nameKg = models.CharField(max_length=500, verbose_name="Название на кыргызском", null=True, blank=True)
    nameEn = models.CharField(max_length=500, verbose_name="Название на английском", null=True, blank=True)

    def __str__(self):
        return self.nameRu

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Категория продукт для продажи фермерам")
        verbose_name_plural = ("Категории продукт для продажи фермерам")


class SaleFarmerItem(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название")
    category = models.ForeignKey(SaleFarmerCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Категория")
    cost = models.FloatField(default=0, verbose_name="Цена")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    image = models.ImageField(null=True, blank=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Продукт для продажи фермерам")
        verbose_name_plural = ("Продукты для продажи фермерам")


class FarmerOrders(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Фермер")
    distributer = models.ForeignKey(Distributer, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Дистрибьютер")
    date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата")
    comment = models.CharField(max_length=200, null=True, blank=True, verbose_name="Комментарий")
    status = FSMIntegerField(choices=utils.OrderStatuses.choices, default=utils.OrderStatuses.New, verbose_name="Статус")
    totalCost = models.IntegerField(default=0, verbose_name="Общая сумма")

    @property
    def items(self):
        return self.cartitems_set.all()

    class Meta:
        verbose_name = ("Заказ")
        verbose_name_plural = ("Заказы")


class CartItems(models.Model):
    """Models for images"""
    order = models.ForeignKey(FarmerOrders, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(SaleFarmerItem, on_delete=models.CASCADE, null=True, blank=True,  verbose_name="Товар")
    quantity = models.IntegerField(default=0, verbose_name="Количество")

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name = ("Товар")
        verbose_name_plural = ("Товары")