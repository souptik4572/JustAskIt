from django.http import JsonResponse
from django.db import IntegrityError
from django.utils.decorators import decorator_from_middleware
from rest_framework.decorators import api_view
from rest_framework import status
from ..serializers import EndUserSerializer, LocationSerializer, EducationSerializer, EmploymentSerializer
from ..models import EndUser, Location, Education, Employment, Follow
from django.views.decorators.csrf import csrf_exempt
import json
import bcrypt
import jwt
from datetime import datetime, timedelta
from decouple import config
from ...middleware.auth_strategy import AuthStrategyMiddleware

ACCESS_SECRET_TOKEN = config('ACCESS_SECRET_TOKEN')
BCRYPT_SALT = int(config('BCRYPT_SALT'))


def hash_password(password):
    return str(bcrypt.hashpw(
        password.encode('utf-8'), bcrypt.gensalt(BCRYPT_SALT))).replace("b'", "").replace("'", "")


def check_password(given_password, actual_password):
    return bcrypt.checkpw(given_password.encode('utf-8'), actual_password.encode('utf-8'))

# Create your views here.


@csrf_exempt
@api_view(['PATCH'])
@decorator_from_middleware(AuthStrategyMiddleware)
def edit_user_profile(request):
    data = json.loads(request.body)
    try:
        endUser = EndUser.objects.get(pk=request.user.id)
        if 'name' in data:
            endUser.name = data['name']
        if 'email' in data:
            endUser.email = data['email']
        if 'phone' in data:
            endUser.phone = data['phone']
        if 'description' in data:
            endUser.description = data['description']
        if 'profile_image' in data:
            endUser.profile_image = data['profile_image']
        endUser.save()
        return JsonResponse({
            'success': True,
            'message': 'Successfully updated data'
        })
    except EndUser.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'User with given email does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['GET'])
@decorator_from_middleware(AuthStrategyMiddleware)
def get_user_profile(request):
    try:
        endUser = EndUser.objects.get(pk=request.user.id)
        endUserData = EndUserSerializer(endUser).data
        endUserData['followers'] = Follow.objects.filter(followee__id=endUser.id).count()
        endUserData['following'] = Follow.objects.filter(follower__id=endUser.id).count()
        endUserData['location'] = LocationSerializer(
            Location.objects.filter(user__id=endUser.id).all(), many=True).data
        endUserData['education'] = EducationSerializer(
            Education.objects.filter(user__id=endUser.id).all(), many=True).data
        endUserData['employment'] = EmploymentSerializer(
            Employment.objects.filter(user__id=endUser.id).all(), many=True).data
        return JsonResponse({
            'success': True,
            'message': 'User profile data',
            'end_user': endUserData
        })
    except EndUser.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'User with given email does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['POST'])
def login_user(request):
    data = json.loads(request.body)
    try:
        email = data['email']
        password = data['password']
        endUser = EndUser.objects.get(email=email)
        if not check_password(password, endUser.password):
            return JsonResponse({
                'success': False,
                'message': 'Passwords do not match'
            }, status=status.HTTP_401_UNAUTHORIZED)
        encoded_token = jwt.encode({
            'id': endUser.id,
            'exp': datetime.now() + timedelta(days=1)
        }, ACCESS_SECRET_TOKEN, algorithm='HS512')
        return JsonResponse({
            'success': True,
            'message': 'successfully logged in',
            'token': encoded_token
        }, status=status.HTTP_200_OK)
    except KeyError:
        return JsonResponse({
            'success': False,
            'message': 'Either email or password is missing'
        }, status=status.HTTP_400_BAD_REQUEST)
    except EndUser.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'User with given email does not exist'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


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
            'message': 'Successfully registered end user',
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
