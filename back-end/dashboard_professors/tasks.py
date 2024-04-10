from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from config import settings


@shared_task
def Confirm_Student_Courses(email,firstname,lastname):
    subject = 'Course Confirmation'
    message = f'Hi {firstname} {lastname} Your Courses Confirm by Your Teacher'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

@shared_task
def EmergencyRemove(email,firstname,lastname,status):
    
    if status:
        subject = 'Emergency Delete Course Accept'
        message = f'Hi {firstname} {lastname} Your Courses Confirm by Your Teacher'
    
    subject = 'Emergency Delete Course Rejected'
    message = f'Hi {firstname} {lastname} Your Courses Confirm by Your Teacher'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])



