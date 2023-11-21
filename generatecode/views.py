from segno import make_qr
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import QRCode
from .serializers import QRcodeSerializer
class QRViewSet(viewsets.ModelViewSet):
    queryset  = QRCode.objects.all()
    serializer_class = QRcodeSerializer


    @action(detail=False, methods=['post'])
    def generate_link_qr(self, request):
        link = request.data.get('link')
        qr_code = make_qr(link)
        qr_code_image = qr_code.save('qr_codes/images/qr_code_link.png')

        create_qr = QRCode.objects.create(link=link, qr_code_image=qr_code_image)

        serializer = self.get_serializer(create_qr)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate_email_qr(self, request):
        email = request.data.get('email')
        subject = request.data.get('subject')
        message = request.data.get('message')

        encode = f"mailto:{email}?subject={subject}&body={message}"
        qr_code = make_qr(encode)
        qr_code_image = qr_code.save('qr_codes/images/qr_code_link.png')

        create_qr = QRCode.objects.create(email=email,
                           subject=subject,
                           message=message,
                           qr_code_image=qr_code_image
                        )
        serializer = self.get_serializer(create_qr)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate_text_qr(self, request):
        text = request.data.get('text')
        qr_code = make_qr(text)
        qr_code_image = qr_code.save('qr_codes/images/qr_code_link.png')

        create_qr = QRCode.objects.create(text=text, qr_code_image=qr_code_image)

        serializer = self.get_serializer(create_qr)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate_phone_qr(self, request):
        phone_number = request.data.get('phone_number')
        
        encode = f"tel:{phone_number}"
        qr_code = make_qr(encode)
        qr_code_image = qr_code.save('qr_codes/images/qr_code_link.png')

        create_qr = QRCode.objects.create(phone_number=phone_number, qr_code_image=qr_code_image)

        serializer = self.get_serializer(create_qr)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate_whatsapp_qr(self, request):
        whatsapp_number = request.data.get('whatsapp_number')
        
        encode = f"https://wa.me/{whatsapp_number}"
        qr_code = make_qr(encode)
        qr_code_image = qr_code.save('qr_codes/images/qr_code_link.png')

        create_qr = QRCode.objects.create(whatsapp_number=whatsapp_number, qr_code_image=qr_code_image)

        serializer = self.get_serializer(create_qr)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate_wifi_qr(self, request):
        ssid = request.data.get('ssid')
        network_type = request.data.get('network_type')
        password = request.data.get('password')

        "WPA/WPA2" if network_type.upper() in ['WPA', 'WPA2'] else "nopass"

        
        encode = f"WIFI:T:{network_type};S:{ssid};P:{password};;"
        qr_code = make_qr(encode)
        qr_code_image = qr_code.save('qr_codes/images/qr_code_link.png')

        create_qr = QRCode.objects.create(
            ssid=ssid,
            network_type=network_type,
            password=password,            
            qr_code_image=qr_code_image)

        serializer = self.get_serializer(create_qr)
        return Response(serializer.data)


