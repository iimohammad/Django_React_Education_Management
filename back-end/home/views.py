from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from accounts.permissions import IsAdmin, IsStudent, IsTeacher, IsEducationalAssistant


def login(request):
    user = request.user

    if IsAdmin().has_permission(request, None):  # Check if user is admin
        return redirect('/admin/')
    elif IsStudent().has_permission(request, None):  # Check if user is student
        return redirect('/dashboard_student/')
    elif IsTeacher().has_permission(request, None):  # Check if user is teacher
        return redirect('/dashboard_professors/')
    elif IsEducationalAssistant().has_permission(request, None):  # Check if user is educational assistant
        return redirect(
            'educational_assistant_dashboard')  # Replace 'educational_assistant_dashboard' with the actual URL name
    else:
        # If user role is not recognized, redirect to the login page
        login_url = reverse('rest_framework:login')
        return redirect(login_url)
