import json

from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view

from ...middleware.auth_strategy import AuthStrategyMiddleware
from ..models import Employment, EndUser
from ..serializers import EmploymentSerializer


@csrf_exempt
@api_view(['DELETE'])
@decorator_from_middleware(AuthStrategyMiddleware)
def delete_existing_employment(request, employment_id):
    try:
        existing_employment = Employment.objects.get(
            id=employment_id, user__id=request.user.id)
        existing_employment.delete()
        return JsonResponse({
            'success': True,
            'message': 'Successfully deleted employment for user'
        }, status=status.HTTP_200_OK)
    except Employment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Employment with given id does not exist'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PATCH'])
@decorator_from_middleware(AuthStrategyMiddleware)
def edit_existing_employment(request, employment_id):
    data = json.loads(request.body)
    try:
        existing_employment = Employment.objects.get(
            id=employment_id, user__id=request.user.id)
        if 'position' in data:
            existing_employment.position = data['position']
        if 'company' in data:
            existing_employment.company = data['company']
        if 'start_year' in data:
            existing_employment.start_year = data['start_year']
        if 'end_year' in data:
            existing_employment.end_year = data['end_year']
        return JsonResponse({
            'success': True,
            'message': 'Successfully updated existing employment data',
            'employment': EmploymentSerializer(existing_employment).data
        }, status=status.HTTP_202_ACCEPTED)
    except Employment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Employment with given id does not exist'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PUT'])
@decorator_from_middleware(AuthStrategyMiddleware)
def add_new_employment(request):
    data = json.loads(request.body)
    try:
        position = data['position']
        company = data['company']
        start_year = data['start_year']
        end_year = None
        if 'end_year' in data:
            end_year = data['end_year']
        employment_count = Employment.objects.filter(
            user__id=request.user.id).count()
        if employment_count >= 3:
            return JsonResponse({
                'success': False,
                'message': 'Only recent 3 employment data are allowed. Please delete other employments and then add new one'
            }, status=status.HTTP_403_FORBIDDEN)
        endUser = request.user
        new_employment = Employment.objects.create(
            user=endUser, position=position, company=company, start_year=start_year, end_year=end_year)
        return JsonResponse({
            'success': True,
            'message': 'Successfully added new employment data',
            'employment': EmploymentSerializer(new_employment).data
        }, status=status.HTTP_201_CREATED)
    except KeyError:
        return JsonResponse({
            'success': False,
            'message': 'Please provide all data'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)
