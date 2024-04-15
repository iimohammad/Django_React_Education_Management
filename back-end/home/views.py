from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import activate , get_language
from django.utils.translation import gettext_lazy as _
from django.utils import translation
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



# def set_language(request):
#     if request.method == 'POST':
#         language_code = request.POST.get('language')
#         request.session[translation.LANGUAGE_SESSION_KEY] = language_code
#         activate(language_code)
#         return JsonResponse({'success': True})
#     return JsonResponse({'success': False})

def set_language(request):
    language = request.GET.get('language', 'en')

    try:
        activate(language)
        response = JsonResponse({'message': _(f'Language set to {language}')}, status=status.HTTP_200_OK)
        response.set_cookie('django_language', language, max_age=3600, secure=True, httponly=True)
        return response
    except:
        return JsonResponse({'message': _(f'Failed to set {language}')}, status=status.HTTP_406_NOT_ACCEPTABLE)
