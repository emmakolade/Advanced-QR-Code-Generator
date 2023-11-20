from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from .serializers import RegisterSerializer, LoginSerializer, OTPSerializer
from .models import User
from utils import generate_otp, send_otp, send_welcome_email
from utils.messages import SUCCESS, ERROR
import logging
import hashlib
from datetime import timedelta
from django.utils import timezone


logger = logging.getLogger(__name__)


class RegisterView(generics.CreateAPIView):
  queryset = User.objects.none()
  serializer_class = RegisterSerializer

  def perform_create(self, serializer):
    try:
      user = serializer.save()
      otp, expiration_time = generate_otp.generate_otp()
      hashed_otp = hashlib.sha256(otp.encode('utf-8')).hexdigest() 
      
      # salt = bcrypt.gensalt()
      # hashed_otp = bcrypt.hashpw(otp.encode('utf-8'), salt)
      
      user.otp = hashed_otp
      print("OTP", otp)
      user.otp_expiration_time = expiration_time
      user.is_active = False
      user.save()
      # send_otp(user.email, otp, expiration_time)


      logger.info(f'user account created {user.email}')
      return Response({'message': _(SUCCESS['ACCOUNT_CREATED']), }, status=status.HTTP_201_CREATED)
    
    except Exception as e:  
      logger.error(f'{user.email}:user account could not be created: {e}')
      return Response({'message': _(ERROR['ACCOUNT_NOT_CREATED'])}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class VerifyUserView(generics.UpdateAPIView):
  queryset = User.objects.all()
  serializer_class = OTPSerializer

  def update(self, request, *args, **kwargs):
      try:
          user = self.get_object()

          if user.is_active:
            return Response({'message': _(ERROR['USER_ALREADY_VERIFIED'])}, status=status.HTTP_400_BAD_REQUEST)

          serializer = self.get_serializer(data=request.data)
          serializer.is_valid(raise_exception=True)

          entered_otp = serializer.validated_data['otp']
          
          if timezone.now() > user.otp_expiration_time:
            return Response({'message': _(ERROR['OTP_EXPIRED'])}, status=status.HTTP_400_BAD_REQUEST)
          

          hashed_entered_otp = hashlib.sha256(entered_otp.encode('utf-8')).hexdigest()

          if hashed_entered_otp == user.otp and timezone.now() <= user.otp_expiration_time:
            user.is_active = True
            user.save()
            return Response({'message': _(SUCCESS['EMAIL_VERIFIED'])}, status=status.HTTP_200_OK)
          else:
            return Response({'message': _(ERROR['INVALID_OTP'])}, status=status.HTTP_400_BAD_REQUEST)


          # if entered_otp == user.otp and timezone.now() <= user.otp_expiration_time:
          #   user.is_active = True
          #   user.save()
          #   # send_welcome_email(user.email)

          #   logger.info(f'OTP verified {user.email}')
          #   return Response({'message': _(SUCCESS['EMAIL_VERIFIED'])}, status=status.HTTP_200_OK)
          # else:
          #     return Response({'message': _(ERROR['INVALID_OTP'])}, status=status.HTTP_400_BAD_REQUEST)
      except Exception as e:
          logger.error(f'{user.email}:otp could not be verified: {e}')
          return Response({'message': _('otp could not be verified')}, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = OTPSerializer

    def update(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            
            if not user:
                return Response({'message': _(ERROR['USER_NOT_FOUND'])}, status=status.HTTP_404_NOT_FOUND)
            
            if user.is_active:
                return Response({'message': _(ERROR['USER_ALREADY_VERIFIED'])}, status=status.HTTP_400_BAD_REQUEST)
            
            time_since_last_otp = timezone.now() - user.otp_expiration_time

            if time_since_last_otp < timedelta(seconds=30):
                wait_time = 30 - time_since_last_otp.total_seconds()
                return Response({'message': _(f'Please wait {wait_time} seconds before requesting a new OTP.')
                                  },status=status.HTTP_400_BAD_REQUEST)



            otp, expiration_time = generate_otp.generate_otp()
            hashed_otp = hashlib.sha256(otp.encode('utf-8')).hexdigest() 
            user.otp = hashed_otp

            # print("hashed_otp", hashed_otp)
            # print("otp", otp)
            user.otp_expiration_time = expiration_time
            user.save()

            # send_otp(user.email, otp)

            logger.info(f'OTP resent to {user.email}')
            return Response({'message': _(SUCCESS['OTP_RESENT'])}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f'{user.email}: OTP could not be resent: {e}')
            return Response({'message': _('OTP could not be resent')}, status=status.HTTP_400_BAD_REQUEST)



class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            try:
                user = serializer.validated_data['user']
                refresh = RefreshToken.for_user(user)

                logger.info(f'{user.email} logged in successfully.')
                return Response({'token': str(refresh.access_token), 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)

            except serializers.ValidationError as e:
                logger.warning(f"Unsuccessful login attempt: {request.data.get('email')} {e}")
                return Response({'error': _(ERROR['INVALID_CREDENTIALS'])}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({'error':  _(ERROR['INVALID_CREDENTIALS'])}, status=status.HTTP_400_BAD_REQUEST)




    
