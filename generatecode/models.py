from django.db import models
from utils.models import BaseModel

# Create your models here.
class QRCode(BaseModel):
    link = models.URLField(null=False, blank=True)
    qr_code = models.ImageField(null=True, blank=True, upload_to='/qr_codes/images')
    logo = models.ImageField(null=True, blank=True, upload_to='/qr_codes/images')

    email = models.EmailField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    text = models.TextField(null=True, blank=True)
    phone_number = models.CharField(null=True, blank=True, max_length=64)
    whatsapp_number = models.CharField(null=True, blank=True, max_length=64)
    
    ssid = models.CharField(
        null=True,
        blank=True, 
        max_length=300, 
        verbose_name= 'NetworkName'
    )
    password = models.CharField(
        null=True,
        blank=True, 
        max_length=300, 
        verbose_name= 'WifiPassword'
    )
    security = models.CharField(
        null=True,
        blank=True, 
        max_length=300, 
        verbose_name= 'NetworkType'
    )



# class EmailQRCode(BaseModel):
#     email = models.EmailField(null=True, blank=True)
#     subject = models.TextField(null=True, blank=True)
#     message = models.TextField(null=True, blank=True)
