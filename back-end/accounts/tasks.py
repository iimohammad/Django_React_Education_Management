from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from config import settings


@shared_task
def send_verification_code(email, verification_code):
    subject = 'Verification Code'
    message = f'Your verification code is: {verification_code}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


@shared_task
def send_Password_Changed(email):
    subject = 'Password Change Notification'
    message = f'Your password has been changed successfully'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


@shared_task
def send_new_year_email(recipient):
    subject = "Happy New Year"
    current_year = datetime.datetime.now().year
    message = f"""Happy New Year! 🎉 May the coming year be filled with joy, success, 
                and prosperity for you and your loved ones. May it bring new opportunities, 
                exciting adventures, and memorable moments to cherish. 
                Here's to fresh beginnings, renewed hope, and endless possibilities in the year ahead. 
                Wishing you health, happiness, and abundance in {current_year}! 🥳🎆✨"""
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])
