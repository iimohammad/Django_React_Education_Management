from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from config import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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


@shared_task
def send_approval_email(recipient_email):
    subject = 'Employment'
    message = 'Your employment request has been approved.'

    current_dir = os.getcwd()
    pdf_file_path = os.path.join(current_dir, 'generated_pdf.pdf')

    generate_pdf(pdf_file_path)

    with open(pdf_file_path, 'rb') as attachment:
        send_mail(
            subject, message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
            attachments=[('approval.pdf', attachment.read(), 'application/pdf')])

def generate_pdf(file_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    c.drawString(100, 750, "Hello, This is your Employment Degree")
    c.save()