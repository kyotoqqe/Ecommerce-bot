from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE","settings.settings")

app = Celery("settings")

app.config_from_object("django.conf:settings")

app.autodiscover_tasks(["adminappconfig"])

