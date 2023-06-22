from django.urls import path, include
from . import views
from .views import *
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'core'

router = SimpleRouter()

router.register(r'item', views.ItemViewSet)
router.register(r'accepted_product', views.AcceptedViewSet)
router.register(r'payment', views.PaymentViewSet)
router.register(r'news', views.NewsViewSet)
router.register(r'job', views.JobsViewSet)
router.register(r'messages', views.MessagesViewSet)
router.register(r'video', views.VideoViewSet)
router.register(r'slider', views.SliderViewSet)
router.register(r'webproducts', views.WebProductsViewSet)
router.register(r'farmer_sale_category', views.SaleFarmerCategoryViewSet)
router.register(r'farmer_sale_item', views.SaleFarmerItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('synchronization_with_oneC/', views.SyncWithOneCViewSet.as_view())
]
