from django.http import JsonResponse
from django.db import IntegrityError
from django.utils.decorators import decorator_from_middleware
from rest_framework.decorators import api_view
from rest_framework import status
from ..serializers import EndUserSerializer, LocationSerializer, EducationSerializer, EmploymentSerializer
from ..models import EndUser, Location, Education, Employment, Follow, Token
from django.views.decorators.csrf import csrf_exempt
import json
import bcrypt
import jwt
from datetime import datetime, timedelta
from decouple import config
from ...middleware.auth_strategy import AuthStrategyMiddleware
import os
import binascii
from datetime import datetime, timedelta
import pytz

utc = pytz.UTC

ACCESS_SECRET_TOKEN = config('ACCESS_SECRET_TOKEN')
BCRYPT_SALT = int(config('BCRYPT_SALT'))


def hash_item(item, is_password=True):
    item = item.encode('utf-8') if is_password else item
    return str(bcrypt.hashpw(
        item, bcrypt.gensalt(BCRYPT_SALT))).replace("b'", "").replace("'", "")


def check_password(given_password, actual_password):
    return bcrypt.checkpw(given_password.encode('utf-8'), actual_password.encode('utf-8'))

# Create your views here.


@csrf_exempt
@api_view(['GET'])
def get_general_user_profile(request, user_id):
    try:
        endUser = EndUser.objects.get(pk=user_id)
        endUserData = EndUserSerializer(endUser).data
        endUserData['followers'] = Follow.objects.filter(
            followee__id=endUser.id).count()
        endUserData['following'] = Follow.objects.filter(
            follower__id=endUser.id).count()
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
            'message': 'User with given id does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PATCH'])
def update_password(request):
    data = json.loads(request.body)
    try:
        token = data['token']
        user_id = data['user_id']
        password = data['password']
        endUser = EndUser.objects.get(pk=user_id)
        password_reset_token = Token.objects.get(user__id=user_id)
        if utc.localize(datetime.now()) - password_reset_token.created_at > timedelta(days=1):
            password_reset_token.delete()
            return JsonResponse({
                'success': False,
                'message': 'Expired password reset token'
            }, status=status.HTTP_400_BAD_REQUEST)
        if not bcrypt.checkpw(token.encode('utf-8'), password_reset_token.token.encode('utf-8')):
            password_reset_token.delete()
            return JsonResponse({
                'success': False,
                'message': 'Invalid password reset token'
            }, status=status.HTTP_400_BAD_REQUEST)
        hashed_password = hash_item(password)
        endUser.password = hashed_password
        endUser.save()
        password_reset_token.delete()
        return JsonResponse({
            'success': True,
            'message': 'Successfully saved new password'
        }, status=status.HTTP_200_OK)
    except KeyError:
        return JsonResponse({
            'success': False,
            'message': 'Please provide all data'
        }, status=status.HTTP_400_BAD_REQUEST)
    except EndUser.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'User with given id does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Token.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Invalid or expired password reset token'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['POST'])
def request_password_reset(request):
    data = json.loads(request.body)
    try:
        email = data['email']
        endUser = EndUser.objects.get(email=email)
        token = Token.objects.filter(user__id=endUser.id).first()
        if token:
            token.delete()
        reset_token = binascii.b2a_hex(os.urandom(20))
        hash = hash_item(reset_token, False)
        token = Token.objects.create(user=endUser, token=hash)
        return JsonResponse({
            'success': True,
            'token': str(reset_token).replace("b'", "").replace("'", ""),
            'id': endUser.id
        }, status=status.HTTP_200_OK)
    except KeyError:
        return JsonResponse({
            'success': False,
            'message': 'Email data is missing'
        }, status=status.HTTP_400_BAD_REQUEST)
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
@api_view(['PATCH'])
@decorator_from_middleware(AuthStrategyMiddleware)
def edit_user_profile(request):
    data = json.loads(request.body)
    try:
        endUser = request.user
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
        }, status=status.HTTP_202_ACCEPTED)
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
        endUser = request.user
        endUserData = EndUserSerializer(endUser).data
        endUserData['followers'] = Follow.objects.filter(
            followee__id=endUser.id).count()
        endUserData['following'] = Follow.objects.filter(
            follower__id=endUser.id).count()
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
        hashed_password = hash_item(password)
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
