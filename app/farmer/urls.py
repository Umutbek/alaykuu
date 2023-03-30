from django.urls import path, include
from . import views
from .views import *
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'core'

router = SimpleRouter()

router.register(r'order', views.OrderViewSet)
router.register(r'cartItem', views.CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]