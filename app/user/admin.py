from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from django.utils.translation import gettext as _

from user import models


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
                                         'verified', 'payment_left'
                                        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2')
        }),
    )


class DistributorAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ('login', 'phone')
    search_fields = ['login']
    list_filter = (
    )

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        (_('Personal info'), {'fields': ('fullname', 'phone', 'avatar', 'passport_front',
                                         'passport_back', 'passport_text', 'city', 'district',
                                         'address', 'comment', 'active', 'rating'
                                        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2')
        }),
    )


class AlaykuuAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ('login',)
    search_fields = ['login']
    list_filter = (
    )

    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        (_('Personal info'), {'fields': ('fullname', 'phone', 'avatar', 'passport_front',
                                         'passport_back', 'passport_text', 'city', 'district',
                                         'address', 'comment', 'active', 'rating', 'access_level'
                                        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2')
        }),
    )

admin.site.register(models.Farmer, FarmerAdmin)
admin.site.register(models.Distributer, DistributorAdmin)
admin.site.register(models.CompanyUser, AlaykuuAdmin)
admin.site.register(models.City)
admin.site.register(models.District)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)


