from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware, decorator_from_middleware_with_args
from rest_framework.decorators import api_view
from rest_framework import status
from api.constants.ask_type_constants import LIMITED
from api.user.models import Follow
from .serializers import CommentSerializer
from .models import Comment
from ..answer.models import Answer
from django.views.decorators.csrf import csrf_exempt
import json
from ..middleware.auth_strategy import AuthStrategyMiddleware

# Create your views here.


@csrf_exempt
@api_view(['GET'])
@decorator_from_middleware_with_args(AuthStrategyMiddleware)(False)
def get_all_comments_to_particular_comment(request, comment_id):
    try:
        the_comment = Comment.objects.get(id=comment_id)
        if request.user is None:
            if the_comment.answer.question.ask_type == LIMITED:
                return JsonResponse({
                    'success': False,
                    'message': 'Access blocked to unauthorized user'
                }, status=status.HTTP_401_UNAUTHORIZED)
            comments = Comment.objects.filter(comment__id=comment_id).all()
        else:
            if not (Follow.objects.filter(followee=the_comment.answer.question.owner.id, follower=request.user.id).exists() and
                    the_comment.answer.question.ask_type == LIMITED and
                    the_comment.answer.question.owner.id != request.user.id):
                return JsonResponse({
                    'success': False,
                    'message': 'Question is limited and can only be accessed by followers of the owner'
                }, status=status.HTTP_401_UNAUTHORIZED)
            comments = Comment.objects.filter(comment__id=comment_id)
        return JsonResponse({
            'success': True,
            'message': f"All comments of a particular answer with id {comment_id}",
            'comments': CommentSerializer(comments, many=True).data
        }, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Comment does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['GET'])
@decorator_from_middleware_with_args(AuthStrategyMiddleware)(False)
def get_all_comments_to_particular_answer(request, answer_id):
    try:
        the_answer = Answer.objects.get(id=answer_id)
        if request.user is None:
            if the_answer.question.ask_type == LIMITED:
                return JsonResponse({
                    'success': False,
                    'message': 'Access blocked to unauthorized user'
                }, status=status.HTTP_401_UNAUTHORIZED)
            comments = Comment.objects.filter(answer__id=answer_id).all()
        else:
            if not (Follow.objects.filter(followee=the_answer.question.owner.id, follower=request.user.id).exists() and
                    the_answer.question.ask_type == LIMITED and
                    the_answer.question.owner.id != request.user.id):
                return JsonResponse({
                    'success': False,
                    'message': 'Question is limited and can only be accessed by followers of the owner'
                }, status=status.HTTP_401_UNAUTHORIZED)
            comments = Comment.objects.filter(answer__id=answer_id)
        return JsonResponse({
            'success': True,
            'message': f"All comments of a particular answer with id {answer_id}",
            'comments': CommentSerializer(comments, many=True).data
        }, status=status.HTTP_200_OK)
    except Answer.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Answer does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['DELETE'])
@decorator_from_middleware(AuthStrategyMiddleware)
def delete_existing_comment(request, comment_id):
    try:
        existing_comment = Comment.objects.get(
            id=comment_id, owner__id=request.user.id)
        existing_comment.delete()
        return JsonResponse({
            'success': True,
            'message': 'Successfully deleted comment'
        }, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Comment does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PATCH'])
@decorator_from_middleware(AuthStrategyMiddleware)
def edit_existing_comment(request, comment_id):
    data = json.loads(request.body)
    try:
        existing_comment = Comment.objects.get(
            id=comment_id, owner__id=request.user.id)
        if 'comment_text' in data:
            existing_comment.comment_text = data['comment_text']
        existing_comment.save()
        return JsonResponse({
            'success': True,
            'message': 'Successfully updated comment',
            'comment': CommentSerializer(existing_comment).data
        }, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Comment does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PUT'])
@decorator_from_middleware(AuthStrategyMiddleware)
def create_new_comment(request, entity_id):
    data = json.loads(request.body)
    try:
        comment_text = data['comment_text']
        new_comment = Comment.objects.create(
            owner=request.user, comment_text=comment_text)
        if 'to-answer' in request.path:
            answer = Answer.objects.get(id=entity_id)
            new_comment.answer = answer
        elif 'to-comment' in request.path:
            comment = Comment.objects.get(id=entity_id)
            new_comment.comment = comment
        new_comment.save()
        return JsonResponse({
            'success': True,
            'message': 'Successfully created new comment',
            'comment': CommentSerializer(new_comment).data
        }, status=status.HTTP_201_CREATED)
    except KeyError:
        return JsonResponse({
            'success': False,
            'message': 'Please provide all required body parameters'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Answer.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Answer with given id does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Comment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Comment with given id does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)
