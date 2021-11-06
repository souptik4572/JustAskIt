from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import EndUserSerializer
from .models import EndUser
from django.views.decorators.csrf import csrf_exempt
import json
import bcrypt
import jwt
from decouple import config

ACCESS_SECRET_TOKEN = config('ACCESS_SECRET_TOKEN')
BCRYPT_SALT = int(config('BCRYPT_SALT'))


def hash_password(password):
    return str(bcrypt.hashpw(
        password.encode('utf-8'), bcrypt.gensalt(BCRYPT_SALT))).replace("b'", "").replace("'", "")

# Create your views here.


@csrf_exempt
@api_view(['PUT'])
def register_end_user(request):
    data = json.loads(request.body)
    try:
        name = data['name']
        email = data['email']
        phone = data['phone']
        password = data['password']
        description = data['description']
        profile_image = data['profile_image']
        hashed_password = hash_password(password)
        endUser = EndUser.objects.create(name=name, email=email, phone=phone, password=hashed_password,
                                         description=description, profile_image=profile_image)
        return JsonResponse({
            'success': True,
            'message': 'Successfully created end user',
            'end_user': EndUserSerializer(endUser).data
        }, status=status.HTTP_201_CREATED)
    except KeyError:
        return JsonResponse({
            'success': False,
            'message': 'Please provide all data'
        }, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
        return JsonResponse({
            'success': False,
            'message': 'An user with same email already exists'
        }, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)
