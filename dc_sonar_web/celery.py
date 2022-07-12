from __future__ import absolute_import

import os

from celery import Celery
# from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dc_sonar_web.settings')

app = Celery('dc_sonar_web')
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
