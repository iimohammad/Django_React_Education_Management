from celery import shared_task
from django.core.mail import send_mail
from config import settings

@shared_task
def send_verification_code(email, verification_code):
    subject = 'Verification Code'
    message = f'Your verification code is: {verification_code}'
    from_email = settings.EMAIL_HOST_USER 
    send_mail(subject, message, from_email, [email])
