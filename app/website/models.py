from django.db import models
from core import imggenerate, utils
from django_fsm import FSMIntegerField
# Create your models here.


class WebProducts(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название")
    image = models.ImageField(null=True, blank=True, upload_to=imggenerate.all_image_file_path, verbose_name="Фото")
    category = FSMIntegerField(choices=utils.WebProductCategory.choices, verbose_name="Категория")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Товар для ВЕБ")
        verbose_name_plural = ("Товары для ВЕБ")

