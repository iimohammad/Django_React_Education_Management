from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from config import settings


# @shared_task
# def Confirm_Student_Courses(email,firstname,lastname):
#     subject = ''
#     message = f'Hi {firstname} {lastname} Your Courses Confirm by Your Teacher'
#     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


