from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view

from ...middleware.auth_strategy import AuthStrategyMiddleware
from ..models import EndUser, Follow
from ..serializers import EndUserSerializer, FollowSerializer


@csrf_exempt
@api_view(['GET'])
def get_all_followers_general(request, user_id):
    try:
        followers = Follow.objects.filter(
            followee__id=user_id).select_related('follower').all().values('follower')
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
@api_view(['GET'])
def get_all_followees_general(request, user_id):
    try:
        followees = Follow.objects.filter(
            follower__id=user_id).select_related('followee').all().values('followee')
        return JsonResponse({
            'success': True,
            'followees': FollowSerializer(followees, many=True).data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['GET'])
@decorator_from_middleware(AuthStrategyMiddleware)
def get_all_followers(request):
    try:
        followers = Follow.objects.filter(
            followee__id=request.user.id).select_related('follower').all().values('follower')
        return JsonResponse({
            'success': True,
            'followers': FollowSerializer(followers, many=True).data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


# Raw query to fetch follower count of a particular user
# SELECT *, (SELECT COUNT(*) FROM user_follow
#             WHERE follower_id = 1 AND followee_id =   user_enduser.id) AS is_following
# FROM user_enduser
# WHERE id IN (SELECT followee_id FROM user_follow
#                 WHERE follower_id = 3);

@csrf_exempt
@api_view(['GET'])
@decorator_from_middleware(AuthStrategyMiddleware)
def get_all_followees(request):
    try:
        followees = Follow.objects.filter(
            follower__id=request.user.id).select_related('followee').all().values('followee')
        return JsonResponse({
            'success': True,
            'followees': FollowSerializer(followees, many=True).data
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
        follower = request.user
        followee = EndUser.objects.get(pk=user_id)
        Follow.objects.create(follower=follower, followee=followee)
        return JsonResponse({
            'success': True,
            'message': 'Followed given user'
        }, status=status.HTTP_201_CREATED)
    except EndUser.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Followee does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)
