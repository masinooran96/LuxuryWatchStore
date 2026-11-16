"""انتخاب خودکار تنظیمات بر اساس متغیر محیطی DJANGO_ENV.

پیش‌فرض: dev
برای محیط واقعی:
    DJANGO_ENV=prod
"""

import os

ENVIRONMENT = os.environ.get("DJANGO_ENV", "dev").lower()

if ENVIRONMENT in ("prod", "production"):
    from .prod import *  # noqa: F401,F403
elif ENVIRONMENT == "dev":
    from .dev import *  # noqa: F401,F403
else:
    raise ValueError("DJANGO_ENV باید dev یا prod باشد.")
