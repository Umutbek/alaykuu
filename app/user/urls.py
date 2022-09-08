from django.urls import path, include
from . import views
from .views import *
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'user'

router = SimpleRouter()

router.register(r'companyuser', views.CompanyUserViewSet)
router.register(r'farmer', views.FarmerViewSet)
router.register(r'distributer', views.DistributerViewSet)
router.register(r'city', views.CityViewSet)
router.register(r'district', views.DistrictViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path("login/", views.LoginAPI.as_view()),
    path('getme/', views.GetMeView.as_view())
]
