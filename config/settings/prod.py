"""تنظیمات محیط واقعی (Production).

اجرا:
    DJANGO_ENV=prod DJANGO_SECRET_KEY=... DJANGO_ALLOWED_HOSTS=example.com python manage.py runserver
"""

from decouple import Csv, config

from .base import *  # noqa: F401,F403

DEBUG = False

# در محیط واقعی، کلید را از متغیر محیطی بخوان.
SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", cast=Csv())

STATIC_ROOT = BASE_DIR / "staticfiles"

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
