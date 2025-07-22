# SPDX-License-Identifier: AGPL-3.0-or-later
"""
WSGI config for SBtools project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SBtools.settings.development")

application = get_wsgi_application()
