from .base import * 

DEBUG = env.bool("DJANGO_DEBUG", False)

SECRET_KEY= env("SECRET_KEY", default="EUnrJLKwm33xx8g1YQ9qP0QU9dy1S6nP54bs8YrBdHa6P8FF4o7HH32HosEJjq3V",)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1",]



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}