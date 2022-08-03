import datetime
from django.db import models

from django_fsm import FSMIntegerField
import requests
from core import imggenerate, utils
from user.models import Farmer, Distributer


class Item(models.Model):
    """Model for Items"""
    name = models.CharField(max_length=500, verbose_name="Название")
    image = models.ImageField(null=True, blank=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")
    unit = FSMIntegerField(choices=utils.ItemUnit.choices, default=utils.ItemUnit.liter, verbose_name="Измерение")
    type = FSMIntegerField(choices=utils.ItemType.choices, default=utils.ItemType.visible, verbose_name="Тип товара")
    amountleft = models.FloatField(default=0, verbose_name="Оставшаяся сумма")
    issale = models.BooleanField(default=False, verbose_name="Акция?")
    cost = models.FloatField(default=0, verbose_name="Цена товара")
    costSale = models.FloatField(default=0, verbose_name="Акционная цена товара")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Продукт")
        verbose_name_plural = ("Продукты")


class Sort(models.Model):
    """Model for Sort"""
    name = models.CharField(max_length=500, verbose_name="Название cорта")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Сорт")
        verbose_name_plural = ("Сорты")


class Accepted(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True, blank=True)
    distributor = models.ForeignKey(Distributer, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField(default=0, verbose_name="Количество")
    unit = FSMIntegerField(choices=utils.ItemUnit.choices, default=utils.ItemUnit.liter, verbose_name="Измерение")
    unitCost = models.FloatField(default=0)
    discount = models.FloatField(default=0, verbose_name="Скидка")
    totalCost = models.FloatField(default=0, verbose_name="Общая сумма")
    status = FSMIntegerField(choices=utils.AcceptStatus.choices, default=utils.AcceptStatus.paid, verbose_name="Статус оплаты")
    comment = models.CharField(max_length=200, null=True, blank=True, verbose_name="Комментарии")
    sort = models.ForeignKey(Sort, on_delete=models.CASCADE, null=True, blank=True)
    fat = models.FloatField(default=0, verbose_name="Жирность")
    acidity = models.FloatField(default=0, verbose_name="Кислотность")
    date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата")

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Принятый продукт")
        verbose_name_plural = ("Принятые продукты")


class Payment(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата")
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True, blank=True, related_name="payment_farmer")
    totalCost = models.FloatField(default=0, verbose_name="Общая сумма")
    comment = models.CharField(max_length=200, null=True, blank=True, verbose_name="Комментарии")

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Оплата")
        verbose_name_plural = ("Оплаты")


class News(models.Model):
    photo = models.ImageField(null=True, blank=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")
    headline = models.CharField(max_length=200, null=True, blank=True, verbose_name="Заголовок")
    text = models.TextField(null=True, blank=True, verbose_name="Текст")
    date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата")

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Новость")
        verbose_name_plural = ("Новости")


class Job(models.Model):
    jobtitle = models.CharField(max_length=200, null=True, blank=True, verbose_name="Заголовок")
    text = models.TextField(null=True, blank=True, verbose_name="Текст")
    date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата")
    requirements = models.TextField(null=True, blank=True, verbose_name="Требования")
    responsibilities = models.TextField(null=True, blank=True, verbose_name="Обязанности")
    job_conditions = models.TextField(null=True, blank=True, verbose_name="Условия работы")

    def __str__(self):
        return self.jobtitle

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Вакансия")
        verbose_name_plural = ("Вакансии")


class Messages(models.Model):
    fullname = models.CharField(max_length=200, null=True, blank=True, verbose_name="ФИО")
    email = models.EmailField(max_length=200, null=True, blank=True, verbose_name="Почта")
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name="Телефон номер")

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Сообщения")
        verbose_name_plural = ("Сообщении")


class Video(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата")
    video = models.FileField(null=True, blank=True, upload_to=imggenerate.all_image_file_path, verbose_name="Видео")
    thumbnail = models.ImageField(null=True, blank=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Видео")
        verbose_name_plural = ("Видео")


class Slider(models.Model):
    priority = models.IntegerField(default=1, verbose_name="Приоритет")
    photo = models.ImageField(null=True, blank=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Слайдер")
        verbose_name_plural = ("Слайдеры")


class WebProducts(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название")
    image = models.ImageField(null=True, blank=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")
    category = FSMIntegerField(choices=utils.WebProductCategory.choices, verbose_name="Категория")

    def __str__(self):
        return self.name


class SaleFarmerCategory(models.Model):
    nameRu = models.CharField(max_length=500, verbose_name="Название на русском")
    nameKg = models.CharField(max_length=500, verbose_name="Название на кыргызском", null=True, blank=True)
    nameEn = models.CharField(max_length=500, verbose_name="Название на английском", null=True, blank=True)

    def __str__(self):
        return self.nameRu


class SaleFarmerItem(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название")
    category = models.ForeignKey(SaleFarmerCategory, on_delete=models.CASCADE, null=True, blank=True)
    cost = models.FloatField(default=0, verbose_name="Цена")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    image = models.ImageField(null=True, blank=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")

    def __str__(self):
        return self.name