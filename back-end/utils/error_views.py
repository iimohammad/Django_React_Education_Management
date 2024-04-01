from django.http import JsonResponse

def custom_404(request, exception):
    message = "Page not found. The requested URL was not found on this server."
    print(message)
    return JsonResponse({'error': message}, status=404)