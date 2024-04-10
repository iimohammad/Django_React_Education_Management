# education_management/config/celery.py

from __future__ import absolute_import, unicode_literals

import os
from celery.schedules import crontab
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

custom_hour = 12  
custom_minute = 30  


app.conf.beat_schedule = {
    'clear_redis_daily': {
        'task': 'dashboard_student.tasks.clear_redis',
        'schedule': crontab(hour=custom_hour, minute=custom_minute),
    },
}