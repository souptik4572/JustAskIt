from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import EndUser, Location
from ..serializers import LocationSerializer
from django.views.decorators.csrf import csrf_exempt
import json
from ...middleware.auth_strategy import AuthStrategyMiddleware


@csrf_exempt
@api_view(['DELETE'])
@decorator_from_middleware(AuthStrategyMiddleware)
def delete_existing_location(request, location_id):
    try:
        existing_location = Location.objects.get(
            id=location_id, user__id=request.user.id)
        existing_location.delete()
        return JsonResponse({
            'success': True,
            'message': 'Successfully deleted location for an existing user'
        }, status=status.HTTP_200_OK)
    except Location.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Location with given id does not exist'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PATCH'])
@decorator_from_middleware(AuthStrategyMiddleware)
def edit_existing_location(request, location_id):
    data = json.loads(request.body)
    try:
        existing_location = Location.objects.get(
            id=location_id, user__id=request.user.id)
        if 'location' in data:
            existing_location.location = data['location']
        if 'start_year' in data:
            existing_location.start_year = data['start_year']
        if 'end_year' in data:
            existing_location.end_year = data['end_year']
        return JsonResponse({
            'success': True,
            'message': 'Successfully updated existing location data',
            'location': LocationSerializer(existing_location).data
        }, status=status.HTTP_202_ACCEPTED)
    except Location.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Location with given id does not exist'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PUT'])
@decorator_from_middleware(AuthStrategyMiddleware)
def add_new_location(request):
    data = json.loads(request.body)
    try:
        location = data['location']
        start_year = data['start_year']
        end_year = None
        if 'end_year' in data:
            end_year = data['end_year']
        location_count = Location.objects.filter(
            user__id=request.user.id).count()
        if location_count >= 3:
            return JsonResponse({
                'success': False,
                'message': 'Only recent 3 location data are allowed. Please delete other locations and then add new one'
            }, status=status.HTTP_403_FORBIDDEN)
        endUser = EndUser.objects.get(pk=request.user.id)
        new_location = Location.objects.create(
            user=endUser, location=location, start_year=start_year, end_year=end_year)
        return JsonResponse({
            'success': True,
            'message': 'Successfully added new location',
            'location': LocationSerializer(new_location).data
        }, status=status.HTTP_201_CREATED)
    except KeyError:
        return JsonResponse({
            'success': False,
            'message': 'Please provide all data'
        }, status=status.HTTP_400_BAD_REQUEST)
    except EndUser.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'User does not exist'
        }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)
