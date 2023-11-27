from segno import make_qr, make
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import QRCode
from .serializers import QRcodeSerializer
import logging
import os

logger = logging.getLogger(__name__)

class QRViewSet(viewsets.ModelViewSet):
    queryset  = QRCode.objects.all()
    serializer_class = QRcodeSerializer

    @action(detail=False, methods=['post'])
    def generate_link_qr(self, request):
        try:
            link = request.data.get('link')
            qr_code = make_qr(link)

            os.makedirs('qr_codes/images', exist_ok=True)

            image_path = os.path.join('qr_codes/images', f'qr_code_{link}.png')
            qr_code.save(image_path, scale=10)
            create_qr = QRCode.objects.create(link=link, qr_code_image=image_path )

            serializer = self.get_serializer(create_qr)

            # user = request.user.id or None
            # print(user)

            logger.info("QR code link generated")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error generating link QR code: {str(e)}")
            return Response({'error': 'An error occurred while generating QR code.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def generate_email_qr(self, request):
        try:
            email = request.data.get('email')
            subject = request.data.get('subject')
            message = request.data.get('message')

            encode = f"mailto:{email}?subject={subject}&body={message}"
            qr_code = make_qr(encode)

            os.makedirs('qr_codes/images', exist_ok=True)

            image_path = os.path.join('qr_codes/images', f'qr_code_{email}.png')
            qr_code.save(image_path, scale=10)

            create_qr = QRCode.objects.create(email=email,
                            subject=subject,
                            message=message,
                            qr_code_image=image_path
                            )
            serializer = self.get_serializer(create_qr)
            # user = request.user.id

            logger.info("QR code email generated")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error generating email QR code: {str(e)}")
            return Response({'error': 'An error occurred while generating QR code.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def generate_text_qr(self, request):
        try:
            text = request.data.get('text')
            qr_code = make_qr(text)

            os.makedirs('qr_codes/images', exist_ok=True)

            image_path = os.path.join('qr_codes/images', 'qr_code_text.png')
            qr_code.save(image_path, scale=10)

            create_qr = QRCode.objects.create(text=text, qr_code_image=image_path)

            serializer = self.get_serializer(create_qr)
            # user = request.user.id

            logger.info("QR code text generated")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error generating text QR code: {str(e)}")
            return Response({'error': 'An error occurred while generating QR code.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def generate_phone_qr(self, request):
        try:
            phone_number = request.data.get('phone_number')
            # TODO: add country code, check if phone number and country code is valid
            
            encode = f"tel:{phone_number}"
            qr_code = make_qr(encode)
            os.makedirs('qr_codes/images', exist_ok=True)

            image_path = os.path.join('qr_codes/images', 'qr_code_phone.png')
            qr_code.save(image_path, scale=10)

            create_qr = QRCode.objects.create(phone_number=phone_number, qr_code_image=image_path)

            serializer = self.get_serializer(create_qr)
            
            # user = request.user.id

            logger.info("QR code phone generated")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error generating phone QR code: {str(e)}")
            return Response({'error': 'An error occurred while generating QR code.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    @action(detail=False, methods=['post'])
    def generate_whatsapp_qr(self, request):
        try:
            whatsapp_number = request.data.get('whatsapp_number')
            
            encode = f"https://wa.me/{whatsapp_number}"
            qr_code = make_qr(encode)
            os.makedirs('qr_codes/images', exist_ok=True)

            image_path = os.path.join('qr_codes/images', 'qr_code_whatsapp.png')
            qr_code.save(image_path, scale=10)

            create_qr = QRCode.objects.create(whatsapp_number=whatsapp_number, qr_code_image=image_path)

            serializer = self.get_serializer(create_qr)
            # user = request.user.id

            logger.info("QR code whatsapp generated ")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error generating whatsapp QR code : {str(e)}")
            return Response({'error': 'An error occurred while generating QR code.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    @action(detail=False, methods=['post'])
    def generate_wifi_qr(self, request):
        try:
            ssid = request.data.get('ssid')
            network_type = request.data.get('network_type')
            password = request.data.get('password')

            "WPA/WPA2" if network_type.upper() in ['WPA', 'WPA2'] else "nopass"

            
            encode = f"WIFI:T:{network_type};S:{ssid};P:{password};;"
            qr_code = make_qr(encode)
            os.makedirs('qr_codes/images', exist_ok=True)

            image_path = os.path.join('qr_codes/images', 'qr_code_phone.png')
            qr_code.save(image_path, scale=10)

            create_qr = QRCode.objects.create(
                ssid=ssid,
                network_type=network_type,
                password=password,            
                qr_code_image=image_path)

            serializer = self.get_serializer(create_qr)
            # user = request.user.id

            logger.info("QR code wifi generated ")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error generating wifi QR code : {str(e)}")
            return Response({'error': 'An error occurred while generating QR code.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  