from django.http import JsonResponse

def handler404(request,exception):
    message = ('Route not Found')
    response = JsonResponse(date={'error': message})
    response.status_code = 404
    return response

