from SBtools.settings.common import *

SECRET_KEY = '70wv4w$tv1suzuf1-2_h9-p%#!qtsz7%(90x%4a=@3yw6rz%0#'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sponsorblock',
        'USER': 'sponsorblock',
        'PASSWORD': '',
        'HOST': '',
    }
}
