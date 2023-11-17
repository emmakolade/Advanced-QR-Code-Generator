from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from django.utils.translation import gettext_lazy as _
from utils.messages import ERROR

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(max_length=150, min_length=8, write_only=True, label=_("password"))

  class Meta:
    model = User
    fields = ('id', 'email', 'otp', 'password', 'otp_expiration_time')
    read_only_fields = ('id', 'otp', 'otp_expiration_time', 'created_at')

  def validate_email(self, value):
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError(_(ERROR['EMAIL_ALREADY_USED']))
    return value
  
  def create(self, validated_data):
    password = validated_data.pop('password')
    user = User.objects.create_user(**validated_data, password=password)
    return user
  



class OTPSerializer(serializers.Serializer):
  otp = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError('Invalid email or password')
        else:
            raise serializers.ValidationError('Email and password are required')

        attrs['user'] = user
        return attrs



