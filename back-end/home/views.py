from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from accounts.permissions import IsAdmin, IsStudent, IsTeacher, IsEducationalAssistant


def login(request):
    user = request.user

    if IsAdmin().has_permission(request, None):
        return redirect('/admin/')
    elif IsStudent().has_permission(request, None):
        return redirect('/dashboard_student/')
    elif IsTeacher().has_permission(request, None):
        return redirect('/dashboard_professors/')
    elif IsEducationalAssistant().has_permission(request, None):
        return redirect('/dashboard_educationalassistant/')
    else:
        login_url = reverse('rest_framework:login')
        return redirect(login_url)
