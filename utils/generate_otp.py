import random
from django.utils import timezone
from datetime import timedelta

def generate_otp():
    otp = str(random.randint(1000, 9999))
    expiration_time = timezone.now() + timedelta(minutes=10)
    print(otp, expiration_time)
    return otp, expiration_time

# otp, expiration_time = generate_otp()
# print(otp, expiration_time)
