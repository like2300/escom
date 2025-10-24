"""
Production settings for schoolv2 project.
"""
import os
from pathlib import Path
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# For production, specify your actual domain
# Example: ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'localhost']
ALLOWED_HOSTS = ['*']  # Change this to your actual domain in production

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_REDIRECT_EXEMPT = []

# Additional security settings for production
SECURE_SSL_REDIRECT = False  # Set to True if using HTTPS
SESSION_COOKIE_SECURE = True  # Only if using HTTPS
CSRF_COOKIE_SECURE = True  # Only if using HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static files settings for production
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Make sure the static files directory exists
if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)

# Collect static files from all apps
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Storage backend for production (uncomment if using cloud storage like AWS S3)
# from storages.backends.s3boto3 import S3Boto3Storage
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Additional security headers
SECURE_REFERRER_POLICY = 'same-origin'
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Logging configuration for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

print(f"Production settings loaded. Static files will be collected to: {STATIC_ROOT}")