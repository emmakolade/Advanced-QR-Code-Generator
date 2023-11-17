from .views import RegisterView, VerifyUserView, LoginView, ResendOTPView
from django.urls import path

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/<str:pk>/', VerifyUserView.as_view(), name='verify-otp'),
    path('resend-otp/<str:pk>/', ResendOTPView.as_view(), name='resend-otp'),
    path('login/', LoginView.as_view(), name='login'),
]
