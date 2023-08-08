from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from django.utils.translation import gettext as _

from farmer import models


class FarmerAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ('login', 'phone')
    search_fields = ['login']
    list_filter = (
    )

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        (_('Personal info'), {'fields': ('fullname', 'phone', 'avatar', 'passport_front',
                                         'passport_back', 'passport_text', 'city', 'district',
                                         'address', 'comment', 'active', 'rating', 'longitude', 'latitude',
                                         'verified', 'payment_left', 'type'
                                        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2')
        }),
    )


class CartItemsAdmin(admin.StackedInline):
    model = models.CartItems


class ModelOrderAdmin(admin.ModelAdmin):
    inlines = [CartItemsAdmin]

    list_display = ('id', 'farmer', 'date', 'status', 'totalCost')

    fieldsets = (
        (_('Информация о заказе'), {'fields': ('farmer', 'distributer', 'comment',
                                               'totalCost', 'status')}),
    )

admin.site.register(models.Farmer, FarmerAdmin)
# admin.site.register(models.SaleFarmerCategory)
# admin.site.register(models.SaleFarmerItem)
# admin.site.register(models.FarmerOrders, ModelOrderAdmin)
