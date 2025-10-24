"""
Production-ready settings with WhiteNoise for static files
"""
import os
from pathlib import Path
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# For production, specify your actual domain
ALLOWED_HOSTS = ['*']  # You should replace this with your actual domain in production

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

# Static files settings for production using WhiteNoise
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Make sure the static files directory exists
if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)

# Collect static files from all apps
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Add WhiteNoise to middleware for serving static files in production
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise middleware for static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# WhiteNoise settings
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Additional security headers
SECURE_REFERRER_POLICY = 'same-origin'
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

print(f"Production settings loaded with WhiteNoise. Static files will be collected to: {STATIC_ROOT}")