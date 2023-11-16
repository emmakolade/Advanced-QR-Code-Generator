from QRCode.config import base
from django.core.mail import send_mail

def send_welcome_email(email):
  subject = "Hi, There!! welcome "
  message = "Thank you for registering"
  from_email = base.EMAIL_HOST_USER
  recipient_list = [email]
  send_mail(subject, message, from_email, recipient_list, fail_silently=False)