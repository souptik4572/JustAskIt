import json

from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view

from ...middleware.auth_strategy import AuthStrategyMiddleware
from ..models import Education, EndUser
from ..serializers import EducationSerializer


@csrf_exempt
@api_view(['DELETE'])
@decorator_from_middleware(AuthStrategyMiddleware)
def delete_existing_education(request, education_id):
    try:
        existing_education = Education.objects.get(
            id=education_id, user__id=request.user.id)
        existing_education.delete()
        return JsonResponse({
            'success': True,
            'message': 'Successfully deleted education for user'
        }, status=status.HTTP_200_OK)
    except Education.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Education with given id does not exist'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PATCH'])
@decorator_from_middleware(AuthStrategyMiddleware)
def edit_existing_education(request, education_id):
    data = json.loads(request.body)
    try:
        existing_education = Education.objects.get(
            id=education_id, user__id=request.user.id)
        if 'school' in data:
            existing_education.school = data['school']
        if 'degree_type' in data:
            existing_education.degree_type = data['degree_type']
        if 'graduation_year' in data:
            existing_education.graduation_year = data['graduation_year']
        return JsonResponse({
            'success': True,
            'message': 'Successfully updated existing education data',
            'education': EducationSerializer(existing_education).data
        }, status=status.HTTP_202_ACCEPTED)
    except Education.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Education with given id does not exist'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PUT'])
@decorator_from_middleware(AuthStrategyMiddleware)
def add_new_education(request):
    data = json.loads(request.body)
    try:
        school = data['school']
        degree_type = data['degree_type']
        graduation_year = None
        if 'graduation_year' in data:
            graduation_year = data['graduation_year']
        education_count = Education.objects.filter(
            user__id=request.user.id).count()
        if education_count >= 4:
            return JsonResponse({
                'success': False,
                'message': 'Only recent 3 education data are allowed. Please delete other educations and then add new one'
            }, status=status.HTTP_403_FORBIDDEN)
        endUser = request.user
        new_education = Education.objects.create(
            user=endUser, school=school, degree_type=degree_type, graduation_year=graduation_year)
        return JsonResponse({
            'success': True,
            'message': 'Successfully added new education data',
            'education': EducationSerializer(new_education).data
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
