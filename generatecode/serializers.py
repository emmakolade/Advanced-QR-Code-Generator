from .models import QRCode
from rest_framework import serializers

class QRcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = [
            'link',
            'qr_code_image', 
            'logo',
            'email',
            'subject', 
            'message', 
            'text',
            'phone_number', 
            'whatsapp_number', 
            'ssid', 
            'password', 
            'network_type',
            'created_at',
        ]
        
