from django.shortcuts import redirect
from .tasks import send_email_task

def send_email_view(request):
    # Send email asynchronously using Celery task
    subject = 'Subject of the email'
    message = 'Body of the email'
    recipient_email = 'mohammadbaharloo97@yahoo.com'
    send_email_task.delay(subject, message, recipient_email)

    return redirect('/')  
