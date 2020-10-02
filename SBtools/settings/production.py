# SPDX-License-Identifier: AGPL-3.0-or-later
from SBtools.settings.common import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sponsorblock',
        'USER': 'sponsorblock',
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': '',
    }
}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

STATIC_ROOT = os.environ['STATIC_ROOT']
