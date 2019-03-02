"""
WSGI config for jimshoney project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import newrelic.agent
import os

from django.core.wsgi import get_wsgi_application

NEWRELIC_INI=os.getenv('JIM_NEWRELIC_INI', 'JIM')
if os.path.exists(NEWRELIC_INI):
    newrelic.agent.initialize(NEWRELIC_INI)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jimshoney.settings")

application = get_wsgi_application()

