from django.http import JsonResponse
from rest_framework import status
from ..user.models import EndUser
from ..user.serializers import EndUserSerializer
import jwt
from decouple import config

ACCESS_SECRET_TOKEN = config('ACCESS_SECRET_TOKEN')


class AuthStrategyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    # process_view is called before the view is called
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            token = request.headers.get(
                'Authorization', None).split(' ')[1]
            verified_user = jwt.decode(
                token, ACCESS_SECRET_TOKEN, algorithms=['HS512'])
            request.user = EndUser.objects.get(pk=verified_user['id'])
            # If None is returned the request flow proceeds to the view
            return None
        except jwt.InvalidTokenError:
            return JsonResponse({
                'success': False,
                'message': 'Token is invalid'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.ExpiredSignatureError:
            return JsonResponse({
                'success': False,
                'message': 'Token is expired'
            }, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return JsonResponse({
                'success': False,
                'message': 'Auth Token not provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_404_NOT_FOUND)
