from rest_framework import serializers
from django.contrib.auth import authenticate
from django.conf import settings
from .models import User
from django.core.exceptions import ObjectDoesNotExist
import jwt
from django.utils.translation import gettext_lazy as _
from utils.messages import ERROR

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(_("password"), max_length=150, min_length=8, write_only=True)

  class Meta:
    model = User
    fields = ('id', 'email', 'otp')
    read_only_fields = ('id', 'otp')

  def validate_email(self, value):
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError(_(ERROR['EMAIL_ALREADY_USED']))
    return value
  
  def create(self, validated_data):
    password = validated_data.pop('password')
    user = User.objects.create_user(**validated_data, password=password)
    return user


