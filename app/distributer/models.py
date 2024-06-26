from django.db import models
from user.models import User
from core import imggenerate


class Distributer(User):
    """Model for distributer"""

    # def save(self):
    #     if self.type == None:
    #         self.type = 3
    #     else:
    #         pass
    #     super(Distributer, self).save()

    class Meta:
        ordering = ('-id',)
        verbose_name = ("Распределитель")
        verbose_name_plural = ("Распределители")

    oneC_id = models.CharField(max_length=256, null=True, blank=True, verbose_name='1С ID')