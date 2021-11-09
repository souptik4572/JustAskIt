from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import EndUser, Follow
from ..serializers import FollowSerializer, EndUserSerializer
from django.views.decorators.csrf import csrf_exempt
from ...middleware.auth_strategy import AuthStrategyMiddleware


@csrf_exempt
@api_view(['GET'])
@decorator_from_middleware(AuthStrategyMiddleware)
def get_all_followers(request):
    try:
        followers = Follow.objects.filter(
            followee=request.user.id).select_related('follower').all().values('follower')
        print(followers[0])
        return JsonResponse({
            'success': True,
            'followers': FollowSerializer(followers, many=True).data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['DELETE'])
@decorator_from_middleware(AuthStrategyMiddleware)
def unfollow_particular_user(request, user_id):
    try:
        follow = Follow.objects.get(
            follower__id=request.user.id, followee=user_id)
        follow.delete()
        return JsonResponse({
            'success': True,
            'message': 'Successfully unfollowed user'
        }, status=status.HTTP_200_OK)
    except Follow.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Follow does not exist'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PUT'])
@decorator_from_middleware(AuthStrategyMiddleware)
def follow_particular_user(request, user_id):
    try:
        follower = EndUser.objects.get(pk=request.user.id)
        followee = EndUser.objects.get(pk=user_id)
        follow = Follow.objects.create(follower=follower, followee=followee)
        return JsonResponse({
            'success': True,
            'message': 'Followed given user'
        }, status=status.HTTP_201_CREATED)
    except EndUser.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Either follower or followee does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)
