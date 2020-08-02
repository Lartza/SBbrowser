from SBtools.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '70wv4w$tv1suzuf1-2_h9-p%#!qtsz7%(90x%4a=@3yw6rz%0#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sponsorblock',
        'USER': 'sponsorblock',
        'PASSWORD': '',
        'HOST': '',
    }
}
