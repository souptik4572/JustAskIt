import jwt
from decouple import config
from django.http import JsonResponse
from rest_framework import status

from ..user.models import EndUser

ACCESS_SECRET_TOKEN = config('ACCESS_SECRET_TOKEN')


class AuthStrategyMiddleware:
    def __init__(self, get_response, is_jwt_required=True):
        self.get_response = get_response
        self.is_jwt_required = is_jwt_required

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
        except AttributeError:
            if not self.is_jwt_required:
                request.user = None
                return None
            return JsonResponse({
                'success': False,
                'message': 'Auth Token not provided'
            }, status=status.HTTP_400_BAD_REQUEST)
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
        except EndUser.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_404_NOT_FOUND)
