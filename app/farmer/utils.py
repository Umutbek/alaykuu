from django.db import models


class OrderStatuses(models.IntegerChoices):
    New = 1, 'Новый'
    Packing = 2, 'Упаковывается'
    Delivering = 3, 'В пути'
    Delivered = 4, 'Доставлено'
    Rejected = 5, 'Отказано'
    ClientReject = 6, 'Отказано'


class FarmerTypes(models.IntegerChoices):
    Small = 1, 'Мелкий'
    Medium = 2, 'Средний'
    Large = 3, 'Крупный'


CASH = 'cash'
CARD = 'card'
PAYMENT_TYPE = ((CARD, 'С картой'), (CASH, 'С наличными'))

MilkCostConst = 30.0
