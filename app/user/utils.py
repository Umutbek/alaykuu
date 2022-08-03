from django.db import models

class UserTypes(models.IntegerChoices):
    USER = 1, 'Пользователь Компании'
    FARMER = 2, 'Фермер'
    DISTRIBUTER = 3, 'Поставшик'