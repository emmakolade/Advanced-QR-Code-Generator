from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from .serializers import RegisterSerializer
from .models import User
from utils import generate_otp, send_otp
from utils.messages import SUCCESS, ERROR
import logging

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
  queryset = User.objects.none()
  serializer_class = RegisterSerializer

  def perform_create(self, serializer):
    try:
      user = serializer.save()
      otp = generate_otp()
      send_otp(user.email, otp)
      user.otp = otp
      user.is_active = False
      user.save()

      data = {
        'id': user.id,
        'email': user.email,
        'otp': user.otp
      }
      
      logger.info(f'user accoutn created {user.email}')
      return Response({'message': _(SUCCESS['ACCOUNT_CREATED']), 'data': data}, status=status.HTTP_201_CREATED)
    
    except Exception as e:  
      logger.error(f'{user.email}:user account could not be created: {e}')
      return Response({'message': _( ERROR['ACCOUNT_NOT_CREATED'])}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




