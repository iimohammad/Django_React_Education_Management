from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from config import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import UnitSelectionRequest
from django_redis import get_redis_connection

@shared_task
def clear_redis():
    try:
        # Connect to Redis
        redis_conn = get_redis_connection('default')

        # Clear the Redis database
        redis_conn.flushdb()

        print('Successfully cleared the Redis database')
    except Exception as e:
        print(f'An error occurred: {str(e)}')
