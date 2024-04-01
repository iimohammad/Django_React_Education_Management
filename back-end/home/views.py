from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from accounts.permissions import (IsAdmin, IsEducationalAssistant, IsStudent,
                                  IsTeacher)


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

