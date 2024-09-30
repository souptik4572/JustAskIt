from django.http import JsonResponse
from rest_framework import status


def handle_success_response(message=None, data=None, status=status.HTTP_200_OK):
    response = {'success': True}
    if message:
        response['message'] = message
    if data:
        response['data'] = data
    return JsonResponse(response, status=status)


def handle_error_response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR):
    return JsonResponse({
        'success': True,
        'message': message
    }, status=status)
