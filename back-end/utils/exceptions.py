from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None or response.status_code == 404:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    return response