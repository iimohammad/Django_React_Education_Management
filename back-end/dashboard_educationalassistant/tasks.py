from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from config import settings


@shared_task
def send_user_pass_for_new_professors(email, username, password, teacher_code):
    subject = 'Educational Assistant Registration'
    message = f'Welcome to X university Your username is: {username}, Your Password is {password} and Your Teacher code is {teacher_code}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

