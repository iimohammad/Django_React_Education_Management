from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from config import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import UnitSelectionRequest

# @shared_task
# def Confirm_Student_Courses(email,firstname,lastname):
#     subject = ''
#     message = f'Hi {firstname} {lastname} Your Courses Confirm by Your Teacher'
#     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])




