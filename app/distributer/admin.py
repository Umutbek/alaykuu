from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from django.utils.translation import gettext as _

from distributer import models
# Register your models here.


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
                                         'address', 'comment', 'active', 'rating', 'type'
                                        )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2')
        }),
    )

admin.site.register(models.Distributer, DistributorAdmin)
