from QRCode.config import base
from django.core.mail import send_mail

def send_otp(email, otp):
  subject = f"Kindly Veryfiy your account with this {otp}"
  message = f"your OTP for registration is {otp}"
  from_email = base.EMAIL_HOST_USER
  recipient_list = [email]
  send_mail(subject, message, from_email, recipient_list, fail_silently=False)