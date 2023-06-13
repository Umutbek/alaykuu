import datetime
from django.db import models

from django_fsm import FSMIntegerField
import requests
from core import imggenerate, utils
from distributer.models import  Distributer
from farmer.models import Farmer
from user.models import District


class Item(models.Model):
    """Model for Items"""
    name = models.CharField(max_length=500, verbose_name="Название")
    image = models.ImageField(null=True, blank=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")
    unit = FSMIntegerField(choices=utils.ItemUnit.choices, default=utils.ItemUnit.liter, verbose_name="Измерение")
    type = FSMIntegerField(choices=utils.ItemType.choices, default=utils.ItemType.visible, verbose_name="Тип товара")
    amountleft = models.FloatField(default=0, verbose_name="Оставшаяся количество")
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
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Товар")
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Фермер")
    distributor = models.ForeignKey(Distributer, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Дистрибьютер")
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
    payment_method = models.CharField(max_length=200, null=True, blank=True, verbose_name="Метод оплаты")
    sync_with_oneC = models.BooleanField('Статус синхронизации с 1С', default=False)

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Принятый продукт")
        verbose_name_plural = ("Принятые продукты")


class Payment(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата")
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True, blank=True, related_name="payment_farmer",
                               verbose_name="Фермер")
    district = models.ForeignKey(District, models.SET_NULL, null=True, blank=True, verbose_name='Район')
    totalCost = models.FloatField(default=0, verbose_name="Общая сумма")
    comment = models.CharField(max_length=200, null=True, blank=True, verbose_name="Комментарий")
    products = models.ManyToManyField(to=Accepted, null=True,
                                      blank=True, verbose_name='Продукты')

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