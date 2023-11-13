from logging import LogRecord
from .base import * 
import cloudinary
import cloudinary.uploader
import cloudinary.api
import logging

from io import BytesIO

cloudinary.config(
    cloud_name='your_cloud_name',
    api_key='your_api_key',
    api_secret='your_api_secret',
    secure = True
)

SECRET_KEY= env("SECRET_KEY")
ALLOWED_HOSTS=[]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "cloudinary": {
            "level": "DEBUG",
            "class": "QRCode.logging.StreamHandler",
            "formatter": "verbose",
        }
    },
   'loggers': {
        'django': {
            'handlers': ['cloudinary'],
            'level': 'INFO',
        },
    },
}

class CloudinaryHandler(logging.Handler):
  def emit(self, record: LogRecord) -> None:
    log_message = self.format(record)

    try:
      res = cloudinary.uploader.upload(
        BytesIO(log_message.encode('utf-8')),
        public_id=f'logs/{record.name}/{record.created}',
        resource_type='raw'
      )
      return res
    except Exception as e:
      return (f" error uploading file to cloudinary: {e}")
    