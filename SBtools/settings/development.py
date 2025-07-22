# SPDX-License-Identifier: AGPL-3.0-or-later
from SBtools.settings.common import *  # noqa

SECRET_KEY = "70wv4w$tv1suzuf1-2_h9-p%#!qtsz7%(90x%4a=@3yw6rz%0#"  # noqa

DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "sponsorblock",
        "USER": "sponsorblock",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}

INTERNAL_IPS = [
    "127.0.0.1",
]
