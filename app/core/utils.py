from django.db import models


class ItemType(models.IntegerChoices):
    visible = 1, 'Активный товар'
    invisible = 2, 'Неактивный товар'

class ItemUnit(models.IntegerChoices):
    kg = 1, 'Килограм'
    liter = 2, 'Литр'
    count = 3, 'Count'
    meter = 4, 'Метр'

class AcceptStatus(models.IntegerChoices):
    paid = 1, 'Заплачено'
    unpaid = 2, 'Незаплачено'


class WebProductCategory(models.IntegerChoices):
    milk = 1, 'Молочная продукция'
    national_beverages = 2, 'Национальные напитки'
    beverages = 3, 'Прохладные напитки'