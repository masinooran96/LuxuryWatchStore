"""تنظیمات محیط توسعه (Development).

اجرا:
    python manage.py runserver
"""

from decouple import config

from .base import *  # noqa: F401,F403

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]

INTERNAL_IPS = ["127.0.0.1"]

# ابزار دیباگ فقط در محیط توسعه فعال می‌شود.
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
