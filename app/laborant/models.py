from django.db import models
from user.models import User
from core import imggenerate


class LaborantUser(User):
    """Model for laborants"""
    class Meta:
        verbose_name = ("Лаборант")
        verbose_name_plural = ("Лаборанты")