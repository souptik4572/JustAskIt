from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import AnswerSerializer
from .models import Answer
from ..question.models import Question
from django.views.decorators.csrf import csrf_exempt
import json
from ..constants.vote_type_constants import UP_VOTE, DOWN_VOTE
from ..middleware.auth_strategy import AuthStrategyMiddleware

# Create your views here.


@csrf_exempt
@api_view(['PUT'])
@decorator_from_middleware(AuthStrategyMiddleware)
def create_new_answer(request, question_id):
    data = json.loads(request.body)
    try:
        answer = data['answer']
        question = Question.objects.get(id=question_id)
        new_answer = Answer.objects.create(
            answer=answer, question=question, owner=request.user)
        return JsonResponse({
            'success': True,
            'message': 'Successfully created new answer',
            'answer': AnswerSerializer(new_answer).data
        }, status=status.HTTP_201_CREATED)
    except KeyError:
        return JsonResponse({
            'success': False,
            'message': 'Answer body parameter not found'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PATCH'])
@decorator_from_middleware(AuthStrategyMiddleware)
def edit_existing_answer(request, answer_id):
    data = json.loads(request.body)
    try:
        existing_answer = Answer.objects.get(
            id=answer_id, owner__id=request.user.id)
        if 'answer' in data:
            existing_answer.answer = data['answer']
        existing_answer.save()
        return JsonResponse({
            'success': True,
            'message': 'Successfully updated answer',
            'question': AnswerSerializer(existing_answer).data
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
def delete_existing_answer(request, answer_id):
    try:
        existing_answer = Answer.objects.get(
            id=answer_id, owner__id=request.user.id)
        existing_answer.delete()
        return JsonResponse({
            'success': True,
            'message': 'Successfully deleted answer',
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
