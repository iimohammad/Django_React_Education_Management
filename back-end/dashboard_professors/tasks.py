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



@shared_task
def send_unit_selection_email(student_email, approval_status):
    subject = "Unit Selection Update"
    if approval_status == "C":
        message = "Your unit selection request needs to be changed. Please check your courses."
    elif approval_status == "R":
        message = "Your unit selection request has been approved."
    else:
        message = "Your unit selection request has been updated."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [student_email])

@shared_task
def send_approval_email(recipient_email):
    subject = 'Your registration request has been approved'
    message = 'Your registration request has been approved.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])

@shared_task
def send_rejection_email(recipient_email):
    subject = 'Your registration request has been rejected'
    message = 'Your registration request has been rejected.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])


@shared_task
def send_DeleteCourse_email(student_email):
    subject = 'Course Deletion Approved'
    message = 'Your request for course deletion has been approved.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [student_email])

@shared_task
def send_Reject_DeleteCourse_email(student_email):
    subject = 'Course Deletion Rejected'
    message = 'Your request for course deletion has been rejected.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [student_email])

@shared_task
def send_semester_delete_approval_email(student_email):
    subject = 'Your semester delete request has been approved'
    message = 'Your semester delete request has been rejected by Teacher.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [student_email])

@shared_task
def send_semester_delete_rejected_email(student_email):
    subject = 'Your semester delete request has been rejected by Teacher'
    message = 'Your semester delete request has been rejected by Teacher.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [student_email])


@shared_task
def send_approved_revision(student_email):
    subject = 'Your revision request has been approved by Teacher.'
    message = 'Your revision request has been approved by Teacher.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [student_email])

@shared_task
def send_rejected_revision(student_email):
    subject = 'Your revision request has been rejected by Teacher'
    message = 'Your revision request has been rejected by Teacher.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [student_email])