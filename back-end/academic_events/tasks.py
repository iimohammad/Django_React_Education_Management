from __future__ import absolute_import, unicode_literals
from datetime import datetime, timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from celery.schedules import crontab
import datetime

@shared_task
def send_email_task(subject, message, recipient):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])

@shared_task
def send_new_year_email(recipient):
    subject = "Happy New Year"
    current_year = datetime.datetime.now().year
    message = f"Happy New Year! 🎉 May the coming year be filled with joy, success, and prosperity for you and your loved ones. May it bring new opportunities, exciting adventures, and memorable moments to cherish. Here's to fresh beginnings, renewed hope, and endless possibilities in the year ahead. Wishing you health, happiness, and abundance in {current_year}! 🥳🎆✨"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])