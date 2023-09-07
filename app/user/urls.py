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
router.register(r'laborant', views.LaborantViewSet)
router.register(r'city', views.CityViewSet)
router.register(r'district', views.DistrictViewSet)
router.register(r'oneC_user', views.OneCUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("login/", views.LoginAPI.as_view()),
    path('getme/', views.GetMeView.as_view()),
    path('password/reset_request/', RequestPasswordResetView.as_view()),
    path('password/reset/', ValidateResetCodeView.as_view()),
    path('change_password/without_old_password/', ChangePasswordWithoutOldPasswordView.as_view(),
         name='change_password_without_old_password')
]
