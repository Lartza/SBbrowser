# SPDX-License-Identifier: AGPL-3.0-or-later
from os import environ
from SBtools.settings.common import * # noqa

SECRET_KEY = environ['SECRET_KEY']

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sponsorblock',
        'USER': 'sponsorblock',
        'PASSWORD': environ['DB_PASSWORD'],
        'HOST': '',
    }
}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

STATIC_ROOT = environ['STATIC_ROOT']
