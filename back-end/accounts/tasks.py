from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from config import settings


@shared_task
def send_verification_code(email, verification_code):
    subject = 'Verification Code'
    message = f'Your verification code is: {verification_code}'
    print(email)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
