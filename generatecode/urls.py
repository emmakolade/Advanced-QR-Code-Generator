from .views import QRViewSet
from django.urls import path, include
from rest_framework.routers import  DefaultRouter

router = DefaultRouter()
router.register(r'qrcodes', QRViewSet, basename='qrcode')

urlpatterns = [
    path('', include(router.urls))
]
